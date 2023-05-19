import React, { useState, useEffect, useRef, useCallback, use } from "react";
import dynamic from 'next/dynamic'
const ReactPlayer = dynamic(() => import("react-player"), { ssr: false });
import { motion, LayoutGroup, AnimatePresence } from "framer-motion";
import DateTime from "react-datetime";
import "react-datetime/css/react-datetime.css";
import VideoPlayer from "../components/VideoPlayer";

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
      <div className='text-black bg-gray-600 w-screen h-screen flex flex-col items-center justify-center'>
        <div class="flex justify-center">
          <div>
            {JSON.stringify(events) != '[]'? events.map(event => (

              <button className="flex flex-row items-center justify-center border-2 border-black rounded-lg m-2 p-2"
              onClick={() => {
                setTime(event.time)
                setSelectedDate(new Date())
              }}
              key={event.time}
              >
                <div>
                  <p>{event.event}</p>
                  <p>{unix_timestamp_to_12hr(event.time)}</p>
                  <p>Duration: {Math.round(event.duration)}</p>
                </div>
              </button>

            )
          
            ): <p>No events to display</p>}
          </div>
          
          <div className='flex flex-col items-center justify-center'>
            <DateTime onChange={handleDateChange} value={selectedDate} />
            <button
              className='m-4 border border-white'
              onClick={() => setSelectedDate(new Date())
              }
            >Use current time</button>
            <p>Selected date: {String(selectedDate)}</p>
            {/* Time: {Time}
            Events: {JSON.stringify(events)}
            VideoUrl : {videoUrl}
            Time to buffer: {time_to_buffer} */}
            <h1 className='text-4xl font-bold'>Enter your time</h1>
            {/* <input
              className='m-16'
              type="text"
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
            /> */}
            <button
              className='m-4 border border-white'
              onClick={handleSubmit}
            >Submit</button>
            {error &&
              <p className='text-red-500'>{error}</p>
            }
          </div>
        </div>
        {videoUrl &&
          <motion.div
            transition={{ duration: 0.5 }}
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            className=''
          >
            {/* <ReactPlayer url={videoUrl}
              ref={playerRef}
              width='75%'
              height='75%'
              controls
              onReady={() => setIsReady(true)}
              /> */}

            <VideoPlayer
              playerRef={playerRef}
              videoUrl={videoUrl}
              setIsReady={setIsReady}
              vidTime={vidTime}
            />

        {/* <div>
          <PlyrPlayer options={options} source={source} />
        </div> */}
          </motion.div>
        }
      </div>
    </AnimatePresence>
  );
}

export default Index;
