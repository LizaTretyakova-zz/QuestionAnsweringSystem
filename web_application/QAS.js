function sendQuery() { 
    var input = document.getElementById("text-field");
    var question = input.value;
    console.log(question);
    input.readOnly = true;
    var answer;
    var answerParagraph = document.getElementById("answer");
    var inProcessInterval;
    var connection = new WebSocket('ws://localhost:9999');
    connection.onopen = function () {
        alert('Sending!');
        answerParagraph.textContent = "In process...";
        inProcessInterval = setInterval(function() {
            answerParagraph.textContent = answerParagraph.textContent + ".";
        }, 4000);
        connection.send(question); // Send the message 'Ping' to the server
    };
    connection.onmessage = function (msg) {
        if (inProcessInterval != undefined) {
            clearInterval(inProcessInterval);
        }
        answer = msg.data;
        answerParagraph = document.getElementById("answer");
        answerParagraph.textContent = answer;
        input.readOnly = false;
    };
}

