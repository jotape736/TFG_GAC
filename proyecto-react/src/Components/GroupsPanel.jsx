import React from 'react'

export function GroupsPanel ({
  selectedSubjectsData,
  selectedGroups,
  setSelectedGroups,
  setShouldFetchSelectedSubjects
}) {
  const organizedData = selectedSubjectsData.reduce((acc, item) => {
    const sigla = item[0][0]
    // console.log('item:', item)
    if (!acc[sigla]) {
      acc[sigla] = []
    }
    return acc
  }, {})

  selectedSubjectsData.forEach((item) => {
    item.forEach((element) => {
      // console.log('element:', element)
      const group = [element[2], element[3], element[4], element[2] + element[3]]
      // cod_asig, letra, nombre, cod_grupo
      organizedData[element[0]].push(group)
    })
  })

  // console.log('Organized Data:', organizedData)

  return (
    <div className='overflow-x-auto mt-2 m-12 w-3/4'>
      <div className='border border-base-300'>
        <table className='table'>
          <thead>
            <tr className='hover'>
              <th className='text-center align-middle bg-base-300'>ASIGNATURA</th>
              <th className='text-center align-middle bg-base-300'>GRUPOS</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(organizedData).map(([sigla, groups]) => (
              <tr key={sigla}>
                <td className='w-70'>{sigla}</td>
                <td className='hover text-center p-0'>
                  <div className='flex flex-wrap '>
                    {groups.map((group, index) => (
                      <div key={index} className='px-4 py-2'>
                        <button
                          className={`btn w-32 ${
                            selectedGroups.includes(group[3]) ? 'btn-primary' : ''}`}
                          title={group[2]}
                          onClick={() => {
                            if (selectedGroups.includes(group[3])) {
                              // console.log('removing', group[3])
                              setSelectedGroups(selectedGroups.filter((g) => g !== group[3]))
                            } else {
                              // console.log('adding', group[3])
                              setSelectedGroups([...selectedGroups, group[3]])
                            }
                          }}
                        >
                          {group[1]}
                        </button>
                      </div>
                    ))}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
