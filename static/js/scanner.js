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
		document.getElementById("identify-btn").style.display = "inline-block"
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

// Show Modal

// Select DOM elements
const showModalBtn = document.querySelector(".show-modal")
const bottomSheet = document.querySelector(".bottom-sheet")
const sheetOverlay = bottomSheet.querySelector(".sheet-overlay")
const sheetContent = bottomSheet.querySelector(".content")
const dragIcon = bottomSheet.querySelector(".drag-icon")

// Global variables for tracking drag events
let isDragging = false,
	startY,
	startHeight

// Show the bottom sheet, hide body vertical scrollbar, and call updateSheetHeight
const showBottomSheet = () => {
	bottomSheet.classList.add("show")
	document.body.style.overflowY = "hidden"
	updateSheetHeight(60)
}

const updateSheetHeight = height => {
	sheetContent.style.height = `${height}vh` //updates the height of the sheet content
	// Toggles the fullscreen class to bottomSheet if the height is equal to 100
	bottomSheet.classList.toggle("fullscreen", height === 100)
}

// Hide the bottom sheet and show body vertical scrollbar
const hideBottomSheet = () => {
	bottomSheet.classList.remove("show")
	document.body.style.overflowY = "auto"
}

// Sets initial drag position, sheetContent height and add dragging class to the bottom sheet
const dragStart = e => {
	isDragging = true
	startY = e.pageY || e.touches?.[0].pageY
	startHeight = parseInt(sheetContent.style.height)
	bottomSheet.classList.add("dragging")
}

// Calculates the new height for the sheet content and call the updateSheetHeight function
const dragging = e => {
	if (!isDragging) return
	const delta = startY - (e.pageY || e.touches?.[0].pageY)
	const newHeight = startHeight + (delta / window.innerHeight) * 100
	updateSheetHeight(newHeight)
}

// Determines whether to hide, set to fullscreen, or set to default
// height based on the current height of the sheet content
const dragStop = () => {
	isDragging = false
	bottomSheet.classList.remove("dragging")
	const sheetHeight = parseInt(sheetContent.style.height)
	sheetHeight < 25
		? hideBottomSheet()
		: sheetHeight > 75
		? updateSheetHeight(100)
		: updateSheetHeight(50)
}

dragIcon.addEventListener("mousedown", dragStart)
document.addEventListener("mousemove", dragging)
document.addEventListener("mouseup", dragStop)

dragIcon.addEventListener("touchstart", dragStart)
document.addEventListener("touchmove", dragging)
document.addEventListener("touchend", dragStop)

sheetOverlay.addEventListener("click", hideBottomSheet)
showModalBtn.addEventListener("click", showBottomSheet)

