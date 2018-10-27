'use strict';

(function() {
  var rate = 10 // Hz
  var socket = io()
  socket.connect('/')
  socket.on('connect', () => {
    console.info('Reisen Socket Bridge connected.')
  })

  socket.on('response', (m) => {
    console.info('response: ' + m )
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

  function setSpeed() {
    let linear = $('#linear').val()
    let angular = $('#angular').val()
    socket.emit('set-speed', linear, angular)
  }
  
  $('#linear, #angular').on('change', setSpeed)
  $('.controller-row > div').on('mousedown touchstart pointerdown', handleKeyDown)
  $('.controller-row > div').on('mouseup touchend pointerup', handleKeyUp)
  setSpeed()

})()