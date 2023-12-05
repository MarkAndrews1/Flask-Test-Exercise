class BoggleGame {
    constructor() {
        this.words = new Set()
        this.board = $("#game-container")
        this.score = 0

        this.secs = 60
        this.mainTimer()
        
        this.timer = setInterval(this.countDown.bind(this), 1000)

        $(".word-form", this.board).on("submit", this.wordSubmit.bind(this))
    }

    mainTimer() {
        $(".timer").text(this.secs)
    }

    async countDown() {
        this.secs -= 1
        this.mainTimer()
        if (this.secs === 0) {
            clearInterval(this.timer)
            await this.gameOver()
        }
    }

    showScore(){
        $(".curr-score").text(this.score)
    }


    async gameOver(){
        $(".word-form", this.board).hide()
        const res = await axios.post("/get-score", {score: this.score})
        if (res.data.brokenRec) {
            this.showMsg(` Congratulations!! You Broke Your Record: ${this.score}! :)`)
        }else {
            this.showMsg(`Thank you for playing. Your final score was: ${this.score}`)
        }
    }

    async wordSubmit(e) {
        e.preventDefault()

        const $word = $("#guess-input", this.board)
        const word = $word.val()

        if (!word) {
            return
        }

        if (this.words.has(word)) {
            this.showMsg(`${word} is already found.`)
        }

        const res = await axios.get("/word-check", { params: { word: word } })
        if (res.data.result === 'not-word') {
            this.showMsg(`${word} is not a valid word. :(`)
        } else if (res.data.result === "not-on-board") {
            this.showMsg(`${word} is not on board. :(`)
        } else {
            this.showMsg(`${word} is a valid word. :)`)
            this.appendWord(word)
            this.words.add(word)
            this.score += word.length
            this.showScore()
        }
        console.log(res)
        $word.val('')
    }

    showMsg(msg) {
        $(".msg-p", this.board).text(msg)
    }

    appendWord(word) {
        ("#word-list", this.board).append($(`<li>${word}</li>`))
    }
}

