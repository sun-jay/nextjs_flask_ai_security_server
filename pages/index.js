import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic'
const ReactPlayer = dynamic(() => import("react-player"), { ssr: false });

function VideoPlayer() {
  // const [videoUrl, setVideoUrl] = useState('');
  // const [timeValue, setTimeValue] = useState(0);

  // const handleTimeInputChange = (event) => {
  //   setTimeValue(event.target.value);
  // }

  // const fetchVideoFromQuery = (time) => {
  //   const url = `/query?time=${time}`;
  //   fetch(url)
  //     .then(response => response.json())
  //     .then(data => {
  //       setVideoUrl(data.videoUrl);
  //     });
  // }

  // useEffect(() => {
  //   fetchVideoFromQuery(timeValue);
  // }, [timeValue]);

  return (
    // <div>
    //   <video src={videoUrl} controls />
    //   <input type="number" value={timeValue} onChange={handleTimeInputChange} />
    // </div>
    <ReactPlayer url= 'http://127.0.0.1:5000/query'
    controls />
  );
}

export default VideoPlayer;
