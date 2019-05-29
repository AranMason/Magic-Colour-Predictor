function getColorName(color) {
	switch (color) {
		case 'B':
			return 'Black'
		case 'U':
			return 'Blue'
		case 'R':
			return 'Red'
		case 'G':
			return 'Green'
		case 'W':
			return 'White'
		case 'colorless':
			return 'Colourless'
	}

	return null
}

function getColorIcon(color) {
	switch (color) {
		case 'G':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/8/88/G.svg?version=df0df93e1e913211caca79c573e08235";
		case 'R':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/8/87/R.svg?version=5549fbad7279775e94ad0ae307a289a1";
		case 'B':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/2/2f/B.svg?version=019551d4756f33e6432aaa8dcc0966f8";
		case 'U':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/9/9f/U.svg?version=242e3a0c1616389c9f09510d598dc5c0";
		case 'W':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/8/8e/W.svg?version=4cfe7054aba65596dc7cd79cf9d61d01";
		case 'colorless':
			return "https://gamepedia.cursecdn.com/mtgsalvation_gamepedia/1/1a/C.svg?version=e56220986714ca2913b90a938b196a9e";
	}
}

function toPercent(str) {
	return (parseFloat(str) * 100).toFixed(2) + "%"
}

function loadingPredictionDisplay(text="Loading Predictions"){
	var pred = $("#predictions")
	pred.empty()
	pred.append(`<div id="prediction-loading">${text}</div>`)
}

function initalizePredictionDisplay(res) {
	var pred = $("#predictions");

	Object.keys(res).forEach((item, index) => {
		pred.append(`
							<div id="prediction-color-${item}" class=\"prediction-color\" style="order: ${index}">
								<img class="color-icon" src=\"${getColorIcon(item)}\"""/>
								<div class="color-results">
									${toPercent(res[item])}
								</div>
								<div class="color-bar">
									<div id="prediction-color-${item}-bar" class="prediction-bar" style="width: ${toPercent(res[item]+0.1)}">
									</div>
								</div>
							</div>`)
	})
}

function generatePredictionDisplay(res) {

	console.log("Updating Display");

	var pred = $("#predictions")
	//pred.empty()

	let sorted = Object.keys(res).sort((a, b) => {
		return res[b] - res[a]
	})

	sorted.forEach((item, index) => {
		console.log(item, toPercent(res[item]));

		let percent = toPercent(res[item]);

		let current = $(`div#prediction-color-${item}`)

		current.css('order', index);

		current.children("div.color-bar").children(".prediction-bar").width(percent)

		current.children("div.color-results").text(percent)
	})
}

let base64Image;

initalizePredictionDisplay({
	W: 0,
	U: 0,
	B: 0,
	R: 0,
	G: 0,
	colorless: 0
})

function makePrediction(){
	let message = {
		image: base64Image
	}


	$.post("/api/predict", JSON.stringify(message), (res) => {
		generatePredictionDisplay(res)
	}).fail((xhr, textStatus, errorThrown) => {
		console.log(xhr.responseText);
		loadingPredictionDisplay("File was too large. Try files smaller thant 1MB.")
	})
}

$("#image-selector-input").change(() => {
	//loadingPredictionDisplay();
	let reader = new FileReader();
	reader.onload = (e) => {
		let dataURL = reader.result
		console.log(dataURL)
		$("#image-display").css("background-image", "url(" + dataURL + ")");
		base64Image = dataURL.split(",")[1]

		makePrediction();
	}
	reader.readAsDataURL($("#image-selector-input")[0].files[0])
})

$("#predict-button").click((event) => {
	makePrediction();
})
