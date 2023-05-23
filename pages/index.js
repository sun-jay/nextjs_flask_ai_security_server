import React, { useState, useEffect, useRef, useCallback, use } from "react";
import dynamic from 'next/dynamic'
const ReactPlayer = dynamic(() => import("react-player"), { ssr: false });
import { motion, LayoutGroup, AnimatePresence } from "framer-motion";
import DateTime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import VideoPlayer from "../components/VideoPlayer";
import { FaArrowCircleRight, FaArrowCircleLeft } from "react-icons/fa";
import { AiOutlinePlusCircle } from "react-icons/ai";
import { BsSearch } from "react-icons/bs";

function Index() {
  const [input, setInput] = useState('');
  const [Time, setTime] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);

  const handleDateChange = (date) => {
    setSelectedDate(date._d);
  };

  // handle submit changes time, which calls time useEffect
  // we get the date from the datetime picker, which sets the selectedDate state on change
  // we get the unix timestamp from the selectedDate state
  function handleSubmit() {
    const unixTimestamp = Date.parse(selectedDate) / 1000
    console.log(unixTimestamp);
    // IMPORTANT: we add 3 seconds to account for latency the saved streams(maybe this would have been smarter to account for
    // on the server side, but this is a quick fix)
    setTime(unixTimestamp +3      );
  }


  const [videoData, setVideoData] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState(null);
  const [vidTime, setVidTime] = useState(null);

  // time useEffect
  // if time changes, fetch the video
  // when video is fethced, set isReady to false, and hasBuffered to false, so the player can rebuffer
  // then we log error if we find one
  // then we get the start time of the video from the response header
  // then we get time to buffer by subtracting the start time of the video from the time we want to buffer to
  // then we set the video data to the blob
  useEffect(() => {
    if (Time) {
      setVideoUrl('loading')

      // if err, log no file found
      console.log(`http://192.168.1.101:5000/query?time=${Time}`)
      fetch(`http://192.168.1.101:5000/video?time=${Time}`, 
      // {mode: "cors"}
      )
        .then(response => {
          console.log('res is back') 
          setIsReady(false);
          setHasBuffered(false);   
          // if res is ok, get the start time of the video and the blob, else, log no file found
          if (!response.ok) {
            console.log(response)
            setError("No file found.");
            throw new Error('No file found');
          }else{
            setError(null);
          }
          console.log('time of vis start:', response.headers.get('Content-Disposition'))
          // gets the start time of the video, truancates the decimal
          const vidStart = response.headers.get('Content-Disposition')
          setVidTime(response.headers.get('Content-Disposition'))
          setTime_to_buffer(Time - vidStart)
          return response.blob();
        })
        .then(data => {
          console.log('blob is formed') 
          setVideoData(data);
          console.log('video data is set')
        })
        .catch(err => {
          console.log(err);
        })
    }
  }, [Time]);

  // videoData useEffect
  useEffect(() => {
    setVideoUrl(videoData ? URL.createObjectURL(videoData) : '')
  }, [videoData]);

  const [isPlaying, setIsPlaying] = useState(true);
  const [isReady, setIsReady] = useState(false);
  const playerRef = useRef(null);
  const [time_to_buffer, setTime_to_buffer] = useState(null);
  const [hasBuffered, setHasBuffered] = useState(false);

  // buffer the video to time_to_buffer when the video is ready
  useEffect(() => {
    if (isReady && !hasBuffered) {
      console.log('buffering')
      playerRef.current.seekTo(time_to_buffer, 'seconds');
      setHasBuffered(true);
    }
  }, [isReady, hasBuffered, time_to_buffer]);

  const [curEvent, setCurEvent] = useState(null)
  const [events, setEvents] = useState([])
  // fetch events on page load
  useEffect(() => {
    fetch(`http://192.168.1.101:5000/events`, 
      // {mode: "cors"}
      )
        .then(response => {
          return response.json();
        })
        .then(data => {
          if (data != []) {
            setEvents(data);
          }
        })
        .catch(err => {
          console.log(err);
        })
      setCurEvent(events[0])
  }, []);

  const unix_timestamp_to_12hr = (unix_timestamp) => {
    // var date = new Date(Number(unix_timestamp)*1000);
    // var hours = date.getHours();
    // var minutes = "0" + date.getMinutes();
    // var seconds = "0" + date.getSeconds();
    // var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
    // above is 24hr time, below is 12hr time
    var date = new Date(Number(unix_timestamp)*1000);
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();
    var seconds = "0" + date.getSeconds();
    var ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    var formattedTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2) + ampm;
    return formattedTime
  }


  return (
    <AnimatePresence>
      {/* <div className='text-black bg-gray-600 w-screen h-screen flex  items-center justify-center'> */}
      <div className="flex-row flex flex-auto w-full h-screen border-t-2 text-black bg-gray-200">

        <EventList curEvent={curEvent} setCurEvent={setCurEvent} events={events} setTime={setTime} setSelectedDate={setSelectedDate} unix_timestamp_to_12hr={unix_timestamp_to_12hr}/>

        <div className=" h-screen w-8/12 inline-block bg-gray-500 ">
        <div class="flex flex-col h-full justify-center items-center">
          
          <div className='flex flex-col items-center justify-center'>
          <h1 className='text-4xl mb-4 font-bold'>Enter your time</h1>

          <div className="flex items-center justify-between mb-4">
  <button
    className="m-2 p-1  border-black rounded-lg bg-red-300 hover:bg-blue-600 text-black"
    onClick={handleSubmit}
  >
    <span class="px-7">{'    Submit     '}</span>
  </button>
  <DateTime className="m-1" onChange={handleDateChange} value={selectedDate} />
  <button
    className="m-2 p-1  border-black rounded-lg bg-red-300 hover:bg-blue-600 text-black"
    onClick={() => setSelectedDate(new Date())}
  >
    Use current time
  </button>
</div>

            {/* <p>Selected date: {String(selectedDate)}</p> */}
            {/* Time: {Time}
            Events: {JSON.stringify(events)}
            VideoUrl : {videoUrl}
            Time to buffer: {time_to_buffer} */}
            {/* <input
              className='m-16'
              type="text"
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            /> */}
            
            {error &&
              <p className='text-red-500'>{error}</p>
            }

          <div className='flex flex-col items-center justify-center h-full w-full'>
            {videoUrl &&
            <motion.div
              transition={{ duration: 0.5 }}
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "100%" }}
              className='w-10/12'
            >
              {videoUrl == "loading" ?
              <LoadingAnimation />:
              <VideoPlayer
                playerRef={playerRef}
                videoUrl={videoUrl}
                setIsReady={setIsReady}
                vidTime={vidTime}
              />}

            </motion.div>
                    }
          </div>



          </div>
          
        </div>
        
      </div>
        </div>
    </AnimatePresence>
  );
}



const EventList = ({curEvent, setCurEvent,setTime,setSelectedDate, events, unix_timestamp_to_12hr }) => {

  return (
    <div class="relative  border-r-2 overflow-auto h-full w-4/12 inline-block h-full text-black  ">
      <div className="h-full flex flex-col bg-gray-200">
        {/* map list to jsx elemnts */}
        <div
          onClick={() => setCurEvent(null)}
          className={
            curEvent === "AddPrescription"
              ? "hover:bg-red-300 bg-gray-400 border-b-2 border-neutral-700 ease-in duration-100 py-1 "
              : "hover:bg-red-300 bg-gray-400 border-b-2 ease-in border-neutral-700 duration-100 py-1"
          }
        >
          <div className="flex justify-between font-semibold items-center px-4">
            <FaArrowCircleRight
              className={
                curEvent === "AddPrescription"
                  ? "text-gray-400 ease-in duration-400 "
                  : "text-gray-400 ease-in duration-100 opacity-0 "
              }
              size={40}
              opacity={0}
            />
            <div className="flex items-center justify-center p-4  ">
              <div className="p-1">Query Events</div>
              <BsSearch size={25}
              className="ml-2"
               />
            </div>
            <FaArrowCircleRight
              className={
                curEvent === "AddPrescription"
                  ? "text-gray-400 ease-in duration-400 "
                  : "text-gray-400 ease-in duration-100 opacity-0 "
              }
              size={25}
              opacity={0.75}
            />
          </div>
        </div>



        {JSON.stringify(events) != '[]'? [...events].reverse().map(item => (

<button className=
{item == curEvent ? "flex flex-row items-center justify-center border-2 border-black rounded-lg m-2 p-2 hover:bg-gray-400 bg-red-300 border-b-2 border-neutral-700 ease-in duration-100":
"flex flex-row items-center justify-center border-2 border-black rounded-lg m-2 p-2 hover:bg-gray-400 bg-gray-200 border-b-2 border-neutral-700 ease-in duration-100"}
onClick={() => {
  setTime(item.time )
  // we want to set the selected date to the date of the unix timestamp in the form 05/21/2023 2:18 PM
  setSelectedDate(new Date(item.time*1000)  )
  setCurEvent(item)
}}
key={item.time}
>
  <div>
    <p>{item.event == 'person detected'?"Person Detected":''}</p>
    <p>{unix_timestamp_to_12hr(item.time)}</p>
    <p>Duration: {Math.round(item.duration)}</p>
  </div>
</button>

)

): <p>No events to display</p>}
      </div>
    </div>
  );
};



const LoadingAnimation = () => {
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '200px',
  };

  const spinnerStyle = {
    border: '8px solid #f3f3f3', /* Light gray */
    borderTop: '8px solid #3498db', /* Blue */
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    animation: 'spin 1s linear infinite',
  };

  const textStyle = {
    marginTop: '16px',
  };

  return (
    <div className="flex flex-col items-center justify-center h-full w-full">
      <div style={containerStyle}>
        <div style={spinnerStyle}></div>
        <div style={textStyle}>Loading...</div>
      </div>
    </div>
  );
};

export default Index;
