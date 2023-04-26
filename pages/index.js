import { useEffect, useState } from "react"
import ReactPlayer from 'react-player';


export default function Home() {
  const [data, setData] = useState({})

  async function get() {
    const info = await fetch('/api/hello', {
      method: 'GET',
    }).then(res => res.json())
    setData(info)
    return info
  }

  useEffect(() => {
    get()
  }, [])

  return (
    <div>
        <div class="h-screen w-screen"> 
          <ReactPlayer
            url='http://127.0.0.1:5000/video'
            className='react-player'
            width='100%'
            height='100%'
            playing={true}
            controls={true}
          />
        </div>


      {/* <img src='http://127.0.0.1:5000/stream4' className="w-12/12 border " alt="logo" /> */}

      {/* <div class="flex w-full h-full">
        <div class="flex flex-col w-6/12 h-full">
          <img src='http://127.0.0.1:5000/stream1' className="w-12/12 border " alt="logo" />
          <img src='http://127.0.0.1:5000/stream2' className="w-12/12 border " alt="logo" />
        </div>
        <div class="flex flex-col w-6/12 h-full">
          <img src='http://127.0.0.1:5000/stream3' className="w-12/12 border " alt="logo" />
          <img src='http://127.0.0.1:5000/stream4' className="w-12/12 border " alt="logo" />
        </div>
      </div> */}
    </div>
  )
}
