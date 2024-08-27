let currentStream
let useFrontCamera = true

async function startCamera() {
	const videoElement = document.getElementById("video")
	const capturedImageElement = document.getElementById("captured-image")
	if (currentStream) {
		currentStream.getTracks().forEach(track => track.stop())
	}
	try {
		const constraints = {
			video: {
				facingMode: useFrontCamera ? "user" : "environment",
			},
		}
		currentStream = await navigator.mediaDevices.getUserMedia(constraints)
		videoElement.style.display = "block" // Show video element
		capturedImageElement.style.display = "none" // Hide captured image
		videoElement.srcObject = currentStream
	} catch (err) {
		console.error("Error accessing the camera:", err)
	}
}

document.addEventListener("DOMContentLoaded", event => {
	startCamera()

	document.getElementById("capture-btn").addEventListener("click", () => {
		const videoElement = document.getElementById("video")
		const capturedImageElement = document.getElementById("captured-image")
		const canvas = document.createElement("canvas")
		canvas.width = videoElement.videoWidth
		canvas.height = videoElement.videoHeight
		const context = canvas.getContext("2d")
		context.drawImage(videoElement, 0, 0, canvas.width, canvas.height)
		const dataUrl = canvas.toDataURL("image/png")
		capturedImageElement.src = dataUrl
		capturedImageElement.style.display = "block" // Show captured image
		videoElement.style.display = "none" // Hide video element
		localStorage.setItem("capturedImage", dataUrl) // Save to local storage
		console.log("Image captured and saved to local storage")

		document.getElementById("capture-btn").style.display = "none"
		document.getElementById("retake-btn").style.display = "inline-block"
		document.getElementById("save-btn").style.display = "inline-block"
	})

	document.getElementById("retake-btn").addEventListener("click", () => {
		startCamera()
		document.getElementById("capture-btn").style.display = "inline-block"
		document.getElementById("retake-btn").style.display = "none"
		document.getElementById("save-btn").style.display = "none"
	})

	document.getElementById("save-btn").addEventListener("click", () => {
		const dataUrl = localStorage.getItem("capturedImage")
		if (dataUrl) {
			const a = document.createElement("a")
			a.href = dataUrl
			a.download = "capture.png"
			a.click()
			console.log("Image saved")
		} else {
			console.log("No image to save")
		}
	})

	document.getElementById("flip-btn").addEventListener("click", () => {
		useFrontCamera = !useFrontCamera
		startCamera()
	})
})
