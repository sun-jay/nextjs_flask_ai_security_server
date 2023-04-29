import ReactPlayer from "react-player/lazy";

export default function VideoPlayer({ playerRef, videoUrl, setIsReady}) {
  return (
    <ReactPlayer
        ref={playerRef}
        url={videoUrl}
        controls={true}
        width='75%'
        height='75%'
        onReady={() => setIsReady(true)}
      />
  );
}