import React, { useState, useEffect, useRef, useCallback } from "react";
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
    setSelectedDate(date);
  };

  function handleKeyDown(event) {
    if (event.keyCode === 13) {
      setCurStart(input);
    }
  }
  function handleSubmit() {
    const unixTimestamp = Date.parse(selectedDate._d) / 1000
    console.log(unixTimestamp);
    setTime(unixTimestamp);
  }

  const [videoData, setVideoData] = useState(null);
  const [videoUrl, setVideoUrl] = useState(null);
  const [error, setError] = useState(null);
  const [vidTime, setVidTime] = useState(null);

  useEffect(() => {
    if (Time) {
      // if err, log no file found
      fetch(`http://127.0.0.1:5000/query?time=${Time}`, 
      // {mode: "cors"}
      )
        .then(response => {
          console.log('res is back')     
          // if res is ok, get the start time of the video and the blob, else, log no file found
          if (!response.ok) {
            setError("No file found.");
            throw new Error('No file found');
          }else{
            setError(null);
          }
          // gets the start time of the video, truancates the decimal
          const vidStart = (response.headers.get('Content-Disposition').split('~')[1].split('.')[0])
          setVidTime(vidStart)
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

  useEffect(() => {
    setVideoUrl(videoData ? URL.createObjectURL(videoData) : '')
  }, [videoData]);



  // const [error, setError] = useState(null);

  // const handleQuery = async (timestamp) => {
  //   try {
  //     const response = await fetch(`/api/query?time=${timestamp}`);

  //     if (response.ok) {
  //       const stream = response.body;
  //       const blob = new Blob([stream], { type: 'video/mp4' });
  //       const url = URL.createObjectURL(blob);
  //       setVideoUrl(url);
  //       setError(null);
  //     } else {
  //       setVideoUrl(null);
  //       setError("No file found.");
  //     }
  //   } catch (err) {
  //     console.error(err);
  //     setVideoUrl(null);
  //     setError("An error occurred while querying the API.");
  //   }
  // };

  // useEffect(() => {
  //   if (Time) {
  //     handleQuery(Time);
  //   }
  // }, [Time]);


  const [isPlaying, setIsPlaying] = useState(true);
  const [isReady, setIsReady] = useState(false);
  const playerRef = useRef(null);
  const [time_to_buffer, setTime_to_buffer] = useState(null);
  const [hasBuffered, setHasBuffered] = useState(false);

  useEffect(() => {
    console.log(playerRef)
    console.log(isReady)
    if (isReady && playerRef.current && !hasBuffered) {
      console.log(' buffering')
      playerRef.current.seekTo(time_to_buffer, 'seconds');
      setHasBuffered(true);
      console.log('buffered')
    }
    
  }, [isReady]);

  

  return (
    <AnimatePresence>
      <div className='text-black bg-gray-600 w-screen h-screen flex flex-col items-center justify-center'>
        <DateTime onChange={handleDateChange} />
        <p>Selected date: {String(selectedDate)}</p>
        Time: {Time}

        VideoUrl : {videoUrl}
        Time to buffer: {time_to_buffer}
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
          </motion.div>
        }
      </div>
    </AnimatePresence>
  );
}

export default Index;
