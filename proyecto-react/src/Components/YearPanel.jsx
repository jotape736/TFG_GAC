import { useState, useEffect } from 'react'
import { SubjectsPanel } from './SubjectsPanel'

export function YearPanel ({ selectedSubjects, setSelectedSubjects, setSelectedSubjectsData }) {
  const [year, setYear] = useState(1)
  const [quarter, setQuarter] = useState(1)
  const [subjects, setSubjects] = useState([]) // Inicializa subjects como un array vacío

  useEffect(() => {
    async function fetchSubjects () {
      try {
        const response = await fetch(
          `http://localhost:5000/asignaturas/curso/${year}/${quarter}`
        )
        const data = await response.json()
        setSubjects(data)
      } catch (error) {
        console.error('Error fetching subjects:', error)
      }
    }

    fetchSubjects()
  }, [year, quarter]) // Dependencia: year. El efecto se ejecuta cada vez que year cambia.

  return (
    <div className='flex flex-col items-center justify-center w-full'>
      <div className='flex justify-around w-4/6'>
        <SelectorQuarter quarter={quarter} setQuarter={setQuarter} setSelectedSubjects={setSelectedSubjects} />
        
        <SelectorYear year={year} setYear={setYear} />
      </div>
      <div className='w-3/4'>
        <SubjectsPanel
          arraySubjects={subjects}
          year={year}
          selectedSubjects={selectedSubjects}
          setSelectedSubjects={setSelectedSubjects}
          quarter={quarter}
        />
      </div>
    </div>
  )
}

function SelectorYear ({ year, setYear }) {
  const years = [1, 2, 3, 4]

  return (
    <div className='flex justify-center items-center mt-4 mb-4 space-x-4'>
      {years.map((yr) => (
        <button
          key={yr}
          onClick={() => {
            setYear(yr)
          }}
          className={`btn btn-outline ${year === yr ? 'btn-active' : 'btn-ghost'}`}
        >
          {yr}º
        </button>
      ))}
    </div>
  )
}

function SelectorQuarter ({ quarter, setQuarter, setSelectedSubjects, setSelectedSubjectsData }) {
  const quarters = [1, 2]

  return (
    <div className='flex justify-center items-center space-x-4'>
      {quarters.map((qtr) => (
        <button
          key={qtr}
          onClick={() => {
            setQuarter(qtr)
            setSelectedSubjects([])
            // setSelectedSubjectsData([])
          }}
          className={`btn btn-outline btn-accent ${quarter === qtr ? 'btn-active' : 'btn-ghost'}`}
        >
          {qtr === 1 ? <span>1<sup>er</sup> Cuatrimestre</span> : <span>{qtr}<sup>o</sup> Cuatrimestre</span>}
        </button>
      ))}
    </div>
  )
}
