import React, { useEffect, useRef, useState } from 'react'
import {
  DayPilot,
  DayPilotCalendar,
  DayPilotNavigator
} from '@daypilot/daypilot-lite-react'
import html2canvas from 'html2canvas'
import './customStyles.css'

const styles = {
  wrap: {
    display: 'flex'
  },
  left: {
    marginRight: '10px'
  },
  main: {
    flexGrow: '1'
  }
}

export function Calendar (selectedSchedules, setSelectedSchedules) {
  const [calendar, setCalendar] = useState(null)
  const [events, setEvents] = useState([])
  const [data, setData] = useState([])
  const [startDate, setStartDate] = useState('2022-08-01')
  const [translatedSchedules, setTranslatedSchedules] = useState([])
  const [currentEventIndex, setCurrentEventIndex] = useState(0) // Add state for current event index

  // DIV CALENDAR DOWNLOADER

  const calendarDivRef = useRef()

  const handleDownload = async () => {
    if (!calendarDivRef.current) return

    // Use html2canvas to capture the screenshot
    const canvas = await html2canvas(calendarDivRef.current)

    // Convert the canvas to a data URL
    const dataURL = canvas.toDataURL('image/png')

    // Create a link element to download the image
    const link = document.createElement('a')
    link.href = dataURL
    link.download = 'downloaded-div.png'
    link.click()
  }

  // END DIV CALENDAR DOWNLOADER

  const config = {
    viewType: 'WorkWeek',
    durationBarVisible: false,
    eventMoveHandling: 'Disabled',
    eventResizeHandling: 'Disabled',
    timeRangeSelectedHandling: 'Disabled',
    headerHeight: 30,
    businessBeginsHour: 8,
    businessEndsHour: 22,
    heightSpec: 'BusinessHoursNoScroll',
    onBeforeCellRender: (args) => {
      const startHour = args.cell.start.getHours()
      if (
        (startHour === 13 && args.cell.start.getMinutes() >= 30) ||
        startHour === 14 ||
        (startHour === 15 && args.cell.start.getMinutes() < 30)
      ) {
        args.cell.properties.backColor = '#dddddd'
      }
    },
    onBeforeHeaderRender: (args) => {
      const daysOfWeek = [
        'DOMINGO',
        'LUNES',
        'MARTES',
        'MIÉRCOLES',
        'JUEVES',
        'VIERNES'
      ]
      args.header.html = daysOfWeek[args.header.start.getDayOfWeek()]
      // args.header.text = args.header.backColor = 'rgba(169, 169, 169)'
    },
    onBeforeEventRender: (args) => {}
  }

  useEffect(() => {
    async function fetchSchedules () {
      const schedulesString = selectedSchedules.selectedSchedules
      const decodedSchedules = decodeURIComponent(schedulesString)
      const url = `http://localhost:5000/horarios?asignaturas=${decodedSchedules}`
      try {
        const response = await fetch(url)
        if (!response.ok) {
          throw new Error('Error fetching translated schedules')
        }
        const data = await response.json()
        setTranslatedSchedules(data)
      } catch (error) {
        console.error('Error fetching translated schedules:', error)
      }
    }

    fetchSchedules()
  }, [selectedSchedules])

  const newEvents = []
  const sideData = []
  useEffect(() => {
    let i = 0
    translatedSchedules.forEach((schedule) => {
      const lista = []
      const dataList = []
      schedule.forEach((item) => {
        dataList.push([item.text.split(')')[0] + ')', item.color]) // Modificación aquí
        lista.push({
          id: i,
          text: item.text,
          start: item.start,
          end: item.end,
          backColor: item.color,
          borderColor: item.borderColor
        // border: '2px solid ' + item.borderColor
        })
        i++
      })

      // Ordenar dataList de la forma deseada
      const sortedDataList = dataList.sort((a, b) => {
        const aText = a[0]
        const bText = b[0]
        const aHasParen = aText.includes('(')
        const bHasParen = bText.includes('(')
        if (aHasParen && !bHasParen) return 1
        if (!aHasParen && bHasParen) return -1
        return aText.localeCompare(bText)
      })

      const uniqueDataList = [...new Set(sortedDataList.map(item => item[0]))].map(text => {
        return sortedDataList.find(item => item[0] === text)
      })
      sideData.push(uniqueDataList)
      newEvents.push(lista)
    })
    setEvents(newEvents[currentEventIndex] || []) // Set events based on current event index
    setData(sideData[currentEventIndex] || [])
  }, [translatedSchedules, currentEventIndex])

  const handleNextEvent = () => {
    setCurrentEventIndex((prevIndex) =>
      prevIndex === translatedSchedules.length - 1
        ? translatedSchedules.length - 1
        : prevIndex + 1
    ) // Increment current event index and wrap around
  }

  const handlePreviousEvent = () => {
    setCurrentEventIndex((prevIndex) =>
      prevIndex === 0
        ? 0
        : (prevIndex - 1 + translatedSchedules.length) %
          translatedSchedules.length
    ) // Decrement current event index and wrap around
  }

  return (
    <div className='w-screen grid grid-cols-12'>
      {/* <div className='flex flex-col col-span-2'>
        <button className='btn w-1/2 self-center' onClick={handleDownload}>Descargar PDF</button>
      </div> */}
      <div className='col-span-8 col-start-3 mb-8'>
        <div ref={calendarDivRef} className='flex justify-between w-full mb-4'>
          {events.length === 0 || data.length === 0
            ? (
              <span />
              )
            : (
              <>
                <span className='flex justify-center items-center text-3xl font-semibold'>
                  Combinación <span className='text-5xl ml-2'>{currentEventIndex + 1}</span>/<span className='text-2xl'>{translatedSchedules.length}</span>
                </span>
                <div style={{ display: 'flex' }}>
                  <button
                    className='btn btn-secondary btn-circle'
                    onClick={handleDownload}
                    style={{ marginRight: '20px' }}
                    title='Descargar horario en PDF'
                  >
                    <svg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke-width='1.5' stroke='currentColor' class='size-6'>
                      <path stroke-linecap='round' stroke-linejoin='round' d='M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3' />
                    </svg>

                  </button>
                  <button
                    className='btn btn-secondary btn-circle'
                    onClick={handlePreviousEvent}
                    style={{ marginRight: '10px' }}
                    title='Combinación anterior'
                  >
                    <svg
                      xmlns='http://www.w3.org/2000/svg'
                      fill='none'
                      viewBox='0 0 24 24'
                      strokeWidth={1.5}
                      stroke='currentColor'
                      className='size-6'
                    >
                      <path
                        strokeLinecap='round'
                        strokeLinejoin='round'
                        d='M10.5 19.5 3 12m0 0 7.5-7.5M3 12h18'
                      />
                    </svg>
                  </button>
                  <button
                    className='btn btn-secondary btn-circle'
                    onClick={handleNextEvent}
                    style={{ marginLeft: '10px' }}
                    title='Siguiente combinación'
                  >
                    <svg
                      xmlns='http://www.w3.org/2000/svg'
                      fill='none'
                      viewBox='0 0 24 24'
                      strokeWidth={1.5}
                      stroke='currentColor'
                      className='size-6'
                    >
                      <path
                        strokeLinecap='round'
                        strokeLinejoin='round'
                        d='M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3'
                      />
                    </svg>
                  </button>
                </div>
              </>
              )}
        </div>
        <div className='flex'>
          <div className='w-full flex justify-center'>
            {events.length === 0 || data.length === 0
              ? (
                <span className='flex self-center loading loading-bars loading-lg' />
                )
              : (
                <DayPilotCalendar
                  {...config}
                  events={events}
                  startDate={startDate}
                  controlRef={setCalendar}
                />
                )}
          </div>
        </div>
      </div>
      <div className='flex flex-col justify-start col-span-2 mt-[64px] ml-4 mr-16'>
        {data && data.map((item, index) => (
          <span className='text-center font-semibold' key={index} style={{ backgroundColor: item[1] }}>
            {item[0]}
          </span>
        ))}
      </div>
    </div>
  )
}
