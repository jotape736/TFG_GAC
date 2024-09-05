import { useState, useEffect } from 'react'
import './App.css'
import logoNegativo1 from './assets/GAC-negativo.svg'
import logoNegativo2 from './assets/GAC-negativo-02.svg'
import logoNegativo3 from './assets/GAC-negativo-03.svg'
import login from './assets/login.svg'
import logoGAC from './assets/GAC.png'
import logoUGR from './assets/UGR-MARCA-02-negativo.png'
import { ThemeController } from './Components/ThemeControler'
import { YearPanel } from './Components/YearPanel'
import { GroupsPanel } from './Components/GroupsPanel'
import { Calendar } from './Components/Calendar'
export function App () {
  const [step, setStep] = useState(0)
  const [selectedSubjects, setSelectedSubjects] = useState([])
  const [selectedSubjectsData, setSelectedSubjectsData] = useState([])
  const [selectedGroups, setSelectedGroups] = useState([])
  const [selectedSchedules, setSelectedSchedules] = useState([])
  const [fetchSelectedSubjectsTrigger, setFetchSelectedSubjectsTrigger] = useState(false)
  const [fetchSelectedGroupsTrigger, setFetchSelectedGroupsTrigger] = useState(false)

  const Ugr = () => {
    return (
      <img src={logoUGR} alt='UGR Logo' style={{ width: '200px', height: 'auto' }} />
    )
  }

  const LogoNegativo3 = () => {
    return (
      <img src={logoNegativo3} alt='GAC Logo' style={{ width: '50px', height: 'auto', marginLeft: '10px' }} />
    )
  }

  const LogoNegativo2 = () => {
    return (
      <img
        src={logoNegativo2}
        alt='GAC Logo'
        style={{ width: '40px', height: 'auto', marginLeft: '10px', marginBottom: '10px', cursor: 'pointer' }}
        onClick={() => { setStep(0); setSelectedSubjects([]) }}
      />
    )
  }

  const LogoNegativo1 = () => {
    return (
      <img src={logoNegativo1} alt='GAC Logo' style={{ width: '50px', height: 'auto', marginLeft: '10px' }} />
    )
  }

  const LogoGAC = () => {
    return (
      <img src={logoGAC} alt='GAC Logo' style={{ width: '250px', height: 'auto' }} />
    )
  }

  const incrementStep = () => {
    setStep(step + 1)
  }

  const Login = () => {
    return (
      <img src={login} alt='Login' style={{ width: '30px', height: 'auto' }} />
    )
  }

  let componentToRender
  // Hacer fetch de las asignaturas seleccionadas para obtener los grupos de teoría.
  // 2961111: [2961111A, 2961111B, ...]
  useEffect(() => {
    async function fetchSelectedSubjects (selectedSubjects) {
      const tempData = []
      try {
        for (const subject of selectedSubjects) {
          const response = await fetch(`http://localhost:5000/teoria/${subject}`)
          const data = await response.json()
          tempData.push(data)
        }
        setSelectedSubjectsData(tempData)
      } catch (error) {
        console.error('Error fetching selected subjects:', error)
      }
    }

    fetchSelectedSubjects(selectedSubjects)
    setFetchSelectedSubjectsTrigger(false)
  }, [fetchSelectedSubjectsTrigger])

  // Hacer fetch de los grupos seleccionados para obtener los subgrupos.
  // 2961111A: [2961111A1, 2961111A2, ...]
  useEffect(() => {
    async function fetchSelectedGroups (selectedGroups) {
      const tempData = []
      try {
        for (const group of selectedGroups) {
          // console.log('Fetching group:', group)
          const response = await fetch(`http://localhost:5000/subgrupos/${group}`)
          const data = await response.json()
          tempData.push(data)
        }

        const tempDataOrganized = tempData.reduce((acc, item) => {
          acc[item[0][0]] = []
          return acc
        }, {})

        tempData.forEach((item) => {
          item.forEach((element) => {
            const key = element[0]
            if (tempDataOrganized[key] && !tempDataOrganized[key].includes(element[1])) {
              tempDataOrganized[key].push(element[1])
            }
          })
        })

        // Convertir la estructura de datos a JSON y luego codificarla para la URL
        const data = encodeURIComponent(JSON.stringify(tempDataOrganized))
        // console.log('Data:', data)
        setSelectedSchedules(data)
      } catch (error) {
        console.error('Error fetching selected groups:', error)
      }
    }

    fetchSelectedGroups(selectedGroups)
  }, [fetchSelectedGroupsTrigger])

  const Header = () => {
    return (
      <div className='flex flex-col items-center'>
        <h1 className='mt-8 my-4 text-2xl font-extrabold leading-none tracking-tight text-base-content md:text-4xl lg:text-5xl text-center'>
          ¡Bienvenido a GAC!
        </h1>
        <h2 className='my-4 text-2xl font-semibold leading-none tracking-tight text-base-content md:text-3xl lg:text-4xl text-center'>
          El Gestor Académico de Calendarios
          {/* TO DO: Añadir curso actual */}
        </h2>
        <div className='flex justify-center'><LogoGAC /></div>
        {/* <h1 className='mt-8 my-4 text-2xl font-extrabold leading-none tracking-tight text-base-content md:text-4xl lg:text-5xl text-center'>
          ¿Qué asignaturas quieres organizar?
        </h1> */}
        <h2 className='my-4 text-2xl font-semibold leading-none tracking-tight text-base-content md:text-3xl lg:text-4xl text-center'>
          Curso 2023/2024
        </h2>
        <details className='dropdown dropdown-down'>
          <summary role='button' className='btn m-1'>Selecciona tu grado</summary>
          <ul tabIndex={0} className='dropdown-content menu bg-base-100 rounded-box z-[1] w-80 p-2 shadow'>
            <li><a onClick={incrementStep}>Ingeniería Informática</a></li>
            <li><a>Ingenierías en Tecnologías de Telecomunicación</a></li>
            <li><a>Ingeniería Informática y Administración y Dirección de Empresas</a></li>
            <li><a>Ingeniería Informática y Matemáticas</a></li>
          </ul>
        </details>
      </div>
    )
  }

  switch (step) {
    case 0:
      componentToRender = (
        <Header />
      )
      break
    case 1:
      componentToRender = (
        <YearPanel
          selectedSubjects={selectedSubjects}
          setSelectedSubjects={setSelectedSubjects}
          setSelectedSubjectsData={setSelectedSubjectsData}
        />
      )
      break
    case 2:
      componentToRender = (
        <GroupsPanel
          selectedSubjectsData={selectedSubjectsData}
          selectedGroups={selectedGroups}
          setSelectedGroups={setSelectedGroups}

        />
      )
      break
    case 3:
      componentToRender = (
        <div className='w-full flex justify-center'>
          <Calendar
            selectedSchedules={selectedSchedules}
            setSelectedSchedules={setSelectedSchedules}
          />
        </div>
      )
      break
    case 4:
      componentToRender = <></>
      break
    default:
      componentToRender = <></>
      break
  }

  return (
    <div className='flex flex-col min-h-screen'>

      <section className='App flex flex-col items-center flex-grow'>
        <nav className='flex justify-between w-full p-4 bg-primary'>

          <div className='text-white flex flex-row'>
            <div className='drawer'>
              <input id='my-drawer' type='checkbox' className='drawer-toggle' />
              <div className='drawer-content'>
                {/* Page content here */}
                <label htmlFor='my-drawer' className='btn btn-primary btn-outline btn-circle drawer-button'><svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' strokeWidth={1.5} stroke='white' className='size-6'>
                  <path strokeLinecap='round' strokeLinejoin='round' d='M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5' />
                                                                                                            </svg>
                </label>
              </div>
              <div className='drawer-side z-50'>
                <label htmlFor='my-drawer' aria-label='close sidebar' className='drawer-overlay' />
                <ul className='menu bg-base-200 text-base-content min-h-full w-80 p-4'>
                  {/* Sidebar content here */}
                  <li><a>Iniciar sesión</a></li>
                  <li><a>Registrarse</a></li>
                  <li><a>Mis horarios</a></li>
                  <li><a>Contacto</a></li>
                  <li><a>Sobre nosotros</a></li>
                  <li><a>Ayuda</a></li>
                </ul>
              </div>
            </div><LogoNegativo2 />

          </div>
          <div className='avatar'>
            <div className='w-12 rounded-full'>
              <img src='https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp' />
            </div>
          </div>
        </nav>

        {step !== 0 && (
          <>
            <div>
              <button
                className={`btn btn-primary m-4 ${step <= 0 ? 'btn-disabled' : ''}`}
                onClick={() => {
                  setStep(step - 1)
                }}
                style={{ width: '140px' }}
              >
                Paso anterior
              </button>

              <button
                className={`btn btn-primary m-4 ${step >= 3 || (step === 2 && selectedGroups.length < 1) || selectedSubjects.length <= 0 ? 'btn-disabled' : ''}`}
                onClick={() => {
                  if (step === 1) {
                    setFetchSelectedSubjectsTrigger(true)
                  } else if (step === 2) {
                    setFetchSelectedGroupsTrigger(true)
                  }
                  setStep(step + 1)
                }}
                style={{ width: '140px' }}
              >
                Siguiente paso
              </button>
            </div>
            <ul className='steps'>
              <li className={`step ${step >= 1 ? 'step-primary' : ''}`}>Selecciona tus asignaturas</li>
              <li className={`step ${step >= 2 ? 'step-primary' : ''}`}>Selecciona tus grupos</li>
              <li className={`step ${step >= 3 ? 'step-primary' : ''}`}>Consulta los horarios</li>
            </ul>
            <div className='divider' />
          </>
        )}

        {componentToRender}
      </section>

      <footer className='flex justify-between items-center w-full p-0 bg-[#4d4c4d]'>
        <div className='pl-2'>
          <Ugr />
        </div>
        <div>
          <p className='text-white pr-2'>
            <strong>TFG Gestor Académico de Calendarios © 2023 - 2024</strong>
          </p>
          <p className='text-white text-center pr-2'>
            Created by{' '}
            <a href='https://github.com/jotape736' target='_blank' rel='noopener noreferrer' className='text-blue-500'>
              José Pablo Márquez
            </a>
          </p>
        </div>
      </footer>
    </div>
  )
}
