'use strict';

(function() {
  var rate = 10 // Hz
  var socket = io()
  socket.connect('/')
  socket.on('connect', () => {
    console.info('Reisen Socket Bridge connected.')
  })

  socket.on('response', (m) => {
    console.info('response: command ' + m + ' received')
  })

  var intervalId = 0
  function handleKeyDown(e) {
    clearInterval(intervalId)
    intervalId = setInterval(() => {
      socket.emit('key-pressed', e.target.id)
    }, 1000 / rate)

  }

  function handleKeyUp() {
    clearInterval(intervalId)
  }

  $('.controller-row > div').on('mousedown touchstart pointerdown', handleKeyDown)
  $('.controller-row > div').on('mouseup touchend pointerup', handleKeyUp)

})()