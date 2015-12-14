

var doAction = (confirmation == false);

if (confirmation) {
	var text = "Do you want to open the calculator?";
	if (language == "de") {
		text = "Wollen Sie den Taschenrechner aufrufen?";
	} else if (language == "ru") {
		text = "Вы хотите открыть калькулятор?";
	}
	doAction = confirm(text);
}

if (doAction) {
	window.open("module:calc.html");
}
