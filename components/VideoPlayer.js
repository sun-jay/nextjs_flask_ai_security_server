import ReactPlayer from "react-player/lazy";

import { useState, useRef, useEffect } from 'react';
// import ReactPlayer from 'react-player/youtube';

export default function VideoPlayer({ playerRef, videoUrl, setIsReady, vidTime }) {
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  function handleProgress({ playedSeconds, played }) {
    setCurrentTime(playedSeconds);
    setDuration(played * duration);
  }

  const getAbsoluteTime = (timeInSeconds) => {
    const unix_timestamp_start_of_video = Number(vidTime)
    // IMPORTANT we subtract 3 seconds to account for the 3 seconds that we added in the request to account for latency
    const totalSeconds = timeInSeconds + (unix_timestamp_start_of_video) 
    const date = new Date(totalSeconds * 1000);
    const formattedTime = date.toLocaleString();
    return formattedTime;
  }

  useEffect(() => {
    console.log('vidTime', vidTime);
  }, [vidTime]);


  const playerProps = {
    ref: playerRef,
    url: videoUrl,
    controls: true,
    width: '100%',
    height: '100%',
    onReady: () => setIsReady(true),
    // config: {
    //   file: {
    //     attributes: {
    //       controlsList: 'nodownload', // Hide the download button
    //     },
    //   },
    // },
    // // light: true, // Hide the poster image
    // config: {
    //   file: {
    //     attributes: {
    //       controlsList: 'nodownload', // Hide the download button
    //     },
    //   },
    // },
    // style: {
    //   pointerEvents: 'none', // Disable seeking and volume controls
    // },
  };

  return (
    <>
      <ReactPlayer {...playerProps} onProgress={handleProgress} />
      <div className="text-white">
        {getAbsoluteTime(currentTime)}
      </div>
    </>
  );
}
