import React from 'react'

export function SubjectsPanel ({
  arraySubjects,
  year,
  selectedSubjects,
  setSelectedSubjects,
  quarter
}) {
  const specialities = ['SI', 'CSI', 'IC', 'TI', 'IS']

  // Determinar el número de columnas basado en el año
  // const columns = year === 3 ? ['TRONCAL', ...specialities] : specialities
  let columns
  if ((year === 3 && quarter === 2) || year === 4) {
    columns = specialities
  } else {
    columns = ['', '', 'TRONCALES', '', '']
  }

  const rows = []

  if (year === 1 || year === 2 || (year === 3 && quarter === 1)) {
  // Para los años 1 y 2, agrupar las asignaturas en filas de hasta 5 elementos
    for (let i = 0; i < arraySubjects.length; i += 5) {
      rows.push(arraySubjects.slice(i, i + 5).map((subject) => [subject[0], subject[3], subject[1]])) // Modificado para incluir subject[4]
    }
  } else {
  // Para los años 3 y 4, agrupar las asignaturas en las columnas correspondientes
    const subjectsByColumns = columns.reduce((acc, column) => {
      acc[column] = []
      return acc
    }, {})

    arraySubjects.forEach((subject) => {
      const columnKey = subject[2] // Subject[3] contiene la clave de la columna
      if (subjectsByColumns[columnKey]) {
        subjectsByColumns[columnKey].push([subject[0], subject[3], subject[1]]) // Modificado para incluir subject[4]
      }
    })

    // Convertir el objeto de columnas a una estructura de filas
    const maxRows = Math.max(
      ...Object.values(subjectsByColumns).map((subjects) => subjects.length)
    )
    for (let i = 0; i < maxRows; i++) {
      rows.push(columns.map((column) => subjectsByColumns[column][i] || ['', ''])) // Modificado para manejar tuplas
    }
  }

  return (
    <div className='overflow-x-auto mt-2 m-12'>
      <div className='border border-base-300'>
        <table className='table'>
          {/* {((year === 3 && quarter === 2) || year === 4) && ( */}
          <thead>
            <tr className='hover'>
              {columns.map((branch, index) => (
                <th
                  key={index} className='text-center align-middle bg-base-300'
                  style={{
                    position: 'sticky',
                    top: 0,
                    zIndex: 1
                  }}
                >
                  {branch}
                </th>
              ))}
            </tr>
          </thead>
          {/* // )} */}
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map(([subjectName, subjectValue, subjectLongName], subjectIndex) => (
                  <td className='hover text-center' key={subjectIndex}>
                    {subjectName && (
                      <button
                        className={`btn w-32 ${
                            selectedSubjects.includes(subjectValue) ? 'btn-primary' : ''
                          }`}
                        onClick={() => {
                          if (selectedSubjects.includes(subjectValue)) {
                            setSelectedSubjects(selectedSubjects.filter(code => code !== subjectValue))
                          } else {
                            setSelectedSubjects([...selectedSubjects, subjectValue])
                          }
                        }}
                        title={subjectLongName}
                      >
                        {subjectName}
                      </button>
                    )}
                  </td>
                ))}
                {(year === 1 || year === 2) &&
        row.length < 5 &&
        // Añadir celdas vacías si la fila tiene menos de 5 asignaturas
        Array.from({ length: 5 - row.length }).map((_, index) => (
          <td key={`empty-${rowIndex}-${index}`} />
        ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
