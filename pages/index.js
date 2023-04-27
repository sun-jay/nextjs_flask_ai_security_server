import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic'
const ReactPlayer = dynamic(() => import("react-player"), { ssr: false });
import { motion, LayoutGroup, AnimatePresence } from "framer-motion";

function VideoPlayer() {
  const [input, setInput] = useState('');
  const [curStart, setCurStart] = useState('');

  function handleKeyDown(event) {
    if (event.keyCode === 13) {
      setCurStart(input);
    }
  }

  return (
    <AnimatePresence>
      <div className='text-black bg-gray-600 w-screen h-screen flex flex-col items-center justify-center'>
        <h1 className='text-4xl font-bold'>Enter your time</h1>
        <input
          className='m-16'
          type="text"
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        {curStart != '' &&
          <motion.div
            transition={{ duration: 0.5 }}
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            className=''
          >
            <ReactPlayer url={`http://127.0.0.1:5000/query?start=${curStart}`}
              controls
              playing
            />
          </motion.div>
        }
      </div>
    </AnimatePresence>
  );
}

export default VideoPlayer;
