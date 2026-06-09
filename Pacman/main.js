const canvas = document.querySelector('canvas')
let ctx = canvas.getContext('2d')
let scoreElem = document.getElementById('scoreDisplay')
let score = 0
let result = document.getElementById('result')
let winElem = document.getElementById('win-text')
let scoreNum = document.getElementById('score-num')
let restartBtn = document.getElementById('restart-btn')
let startBtn = document.getElementById('start-btn')
let startContainer = document.getElementById('start-container')
let startText = document.getElementById('game-intro')
let scoreDisplay = document.getElementById('displayScore')


startBtn.addEventListener('click', function(){
    scoreDisplay.style.visibility = 'visible'
    startContainer.style.visibility = 'hidden'
    startBtn.style.pointerEvents = 'none'

    canvas.width = innerWidth -40 
    canvas.height = innerHeight -80
    
    
    class Boundary{
        static width = 40
        static height = 40
        constructor({position}){
            this.position = position
            this.width = 40
            this.height = 40 
        }
    
        draw(){
            ctx.beginPath()
            ctx.strokeStyle = 'blue';
            ctx.rect(this.position.x,this.position.y,this.width,this.height);
            ctx.stroke();
            ctx.closePath()
        }
    
    }
    
    class Player {
    
        constructor( {position , velocity}){
            this.position = position
            this.velocity = velocity
            this.radius = 15
            this.radians = 0.5
            this.openRate = 0.1
            this.rotation = 0
        }
    
        draw(){
            ctx.save()
            ctx.translate(this.position.x,this.position.y)
            ctx.rotate(this.rotation)
            ctx.translate(-this.position.x,-this.position.y)
            ctx.beginPath()
            ctx.fillStyle = 'yellow'
            ctx.arc(this.position.x,this.position.y,this.radius,this.radians,Math.PI * 2 - this.radians)
            ctx.lineTo(this.position.x,this.position.y)
            ctx.fill()
            ctx.closePath()
            ctx.restore()
        }
    
        update(){
            if (this.radians < 0 || this.radians > 0.75){
                this.openRate *= -1
            }
            this.radians += this.openRate
            this.draw()
            this.position.x += this.velocity.x
            this.position.y += this.velocity.y
        }
    }
    
    class Pellet {
    
        constructor( {position}){
            this.position = position
            this.radius = 5
        }
    
        draw(){
            ctx.beginPath()
            ctx.arc(this.position.x,this.position.y,this.radius,0,Math.PI * 2)
            ctx.fillStyle = 'grey'
            ctx.fill()
            ctx.closePath()
        }
        
    }
    
    class Ghost{
        static speed = 2
        constructor({position,velocity}){
            this.position = position
            this.velocity = velocity
            this.radius = 15
            this.prevCollision = []
            this.speed = 2
            this.scared = false
        }
    
        draw(){
            ctx.beginPath()
            ctx.arc(this.position.x,this.position.y,this.radius,0,Math.PI * 2)
            this.scared ? ctx.fillStyle = 'blue' : ctx.fillStyle = 'red'
            ctx.fill()
            ctx.closePath()
        }
    
        update(){
            this.draw()
            this.position.x += this.velocity.x
            this.position.y += this.velocity.y
        }
    } 
    
    class PowerUps{
    
        constructor( {position} ){
            this.position = position
            this.radius = 7
        }
    
        draw(){
            ctx.beginPath()
            ctx.arc(this.position.x,this.position.y,this.radius,0,Math.PI * 2)
            ctx.fillStyle = 'white'
            ctx.fill()
            ctx.closePath()
        }
        
    }
    
    const map = [
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['-', '.', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '-'],
        ['-', ' ', '-', ' ', '-', '-', '-', ' ', '-', ' ', '-'],
        ['-', ' ', 'p', ' ', ' ', '-', ' ', ' ', ' ', ' ', '-'],
        ['-', ' ', '-', '-', ' ', '&', ' ', '-', '-', ' ', '-'],
        ['-', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', '-'],
        ['-', ' ', '-', ' ', '-', '-', '-', ' ', '-', ' ', '-'],
        ['-', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', ' ', '-'],
        ['-', ' ', '-', '-', ' ', '&', ' ', '-', '-', ' ', '-'],
        ['-', ' ', ' ', ' ', ' ', '-', ' ', ' ', ' ', 'p', '-'],
        ['-', ' ', '-', 'p', '-', '-', '-', ' ', '-', ' ', '-'],
        ['-', ' ', ' ', ' ', ' ', '&', ' ', ' ', ' ', ' ', '-'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
    ]
    const boundaries = []
    const pellets = []
    const ghosts = []
    const powerUps = []
    
    const player = new Player({
        position:{
            x:Boundary.width + (Boundary.width/2),
            y:Boundary.height + (Boundary.height/2)
        },
        velocity:{
            x:0,
            y:0
        }
    })
    
    const keys = {
        ArrowUp:{
            pressed:false
        },
        ArrowDown:{
            pressed:false
        },
        ArrowLeft:{
            pressed:false
        },
        ArrowRight:{
            pressed:false
        }
    }
    
    let lastKey = ''
    
    map.forEach((row,i) => {
        row.forEach((symbol,j) => {
            switch (symbol){
                case '-':
                    boundaries.push(
                        new Boundary({
                            position:{
                                x:Boundary.width * j,
                                y:Boundary.height * i
                            }
                        })
                    )
                    break
    
                case ' ':
                    pellets.push(
                        new Pellet({
                            position:{
                                x:(Boundary.width * j) + (Boundary.width/2),
                                y:(Boundary.height * i) + (Boundary.height/2)
                            }
                        })
                    )
                    break
    
                case '&':
                    ghosts.push(
                        new Ghost({
                            position:{
                                x:(Boundary.width * j) + (Boundary.width/2),
                                y:(Boundary.height * i) + (Boundary.height/2)
                            },
                            velocity:{
                                x:Ghost.speed,
                                y:0
                            }
                        })
                    )
                    break
    
                case 'p':
                        powerUps.push(
                            new PowerUps({
                                position: {
                                    x:(Boundary.width * j) + (Boundary.width/2),
                                    y:(Boundary.height * i) + (Boundary.height/2),
                                }
                            })
                        )
            }
        })
    })
    
    function collisionDetection( {circle, rectangle} ){
        const padding = Boundary.width / 2 - circle.radius -1
        return (
            circle.position.y - circle.radius + circle.velocity.y <= rectangle.position.y + rectangle.height + padding
            && circle.position.x + circle.radius + circle.velocity.x >= rectangle.position.x - padding
            && circle.position.y + circle.radius + circle.velocity.y >= rectangle.position.y - padding
            && circle.position.x - circle.radius + circle.velocity.x  <= rectangle.position.x + rectangle.width + padding
        )
    
    }
    
    function movements(){
        if (keys.ArrowUp.pressed && lastKey === 'ArrowUp'){
    
    
            for (let i=0 ; i<boundaries.length ; i++){
                const boundary = boundaries[i]
    
                if ( collisionDetection( {circle: {...player, velocity: {x:0,y:-5} } , rectangle: boundary} ) ){
                    player.velocity.y = 0
                    break
                }else{
                    player.velocity.y = -5
                }
            }
    
    
        }else if (keys.ArrowDown.pressed && lastKey === 'ArrowDown'){
    
    
            for (let i=0 ; i<boundaries.length ; i++){
                const boundary = boundaries[i]
    
                if ( collisionDetection( {circle: {...player, velocity: {x:0,y:5} } , rectangle: boundary} ) ){
                    player.velocity.y = 0
                    break
                }else{
                    player.velocity.y = 5
                }
            }
    
    
        }else if (keys.ArrowLeft.pressed && lastKey === 'ArrowLeft'){
            
    
            for (let i=0 ; i<boundaries.length ; i++){
                const boundary = boundaries[i]
    
                if ( collisionDetection( {circle: {...player, velocity: {x:-5,y:0} } , rectangle: boundary} ) ){
                    player.velocity.x = 0
                    break
                }else{
                    player.velocity.x = -5
                }
            }
    
    
        }else if (keys.ArrowRight.pressed && lastKey === 'ArrowRight'){
               
    
            for (let i=0 ; i<boundaries.length ; i++){
                const boundary = boundaries[i]
    
                if ( collisionDetection( {circle: {...player, velocity: {x:5,y:0} } , rectangle: boundary} ) ){
                    player.velocity.x = 0
                    break
                }else{
                    player.velocity.x = 5
                }
            }
    
    
        }
    }
    
    function animate(){
    
        let animationId = requestAnimationFrame(animate)
        ctx.clearRect(0,0,canvas.width,canvas.height)
        movements()
    
        boundaries.forEach((boundary) =>{
            boundary.draw()
            if (collisionDetection ({circle:player , rectangle:boundary})){
                player.velocity.x = 0
                player.velocity.y = 0
            }
        })
    
        for (let i=pellets.length - 1 ; 0<=i ; i--) {
            let pellet = pellets[i]
            pellet.draw()
            if (Math.hypot(pellet.position.x - player.position.x,pellet.position.y - player.position.y) < pellet.radius+player.radius){
                pellets.splice(i,1)
                score += 10
                scoreElem.innerHTML = score
            }
        }
    
        if (pellets.length === 0){
            cancelAnimationFrame(animationId)
            winElem.textContent = 'You Win!'
            result.style.visibility = "visible"
            scoreNum.textContent = score
            restartBtn.style.pointerEvents = 'all'
        }
    
        for (let i=powerUps.length - 1 ; 0<=i ; i--) {
            let powerUp = powerUps[i]
            powerUp.draw()
            if (Math.hypot(powerUp.position.x - player.position.x,powerUp.position.y - player.position.y) < powerUp.radius+player.radius){
                powerUps.splice(i,1)
    
                score += 20
    
                ghosts.forEach( (ghost) => {
                    ghost.scared = true
    
                    setTimeout( () => {
                        ghost.scared = false
                    },5000)
                    
                })
            }
        }
    
        for(let i = ghosts.length-1 ; 0<=i ; i--){
            let ghost = ghosts[i]
            if (Math.hypot(ghost.position.x - player.position.x,ghost.position.y - player.position.y) < ghost.radius+player.radius && ghost.scared){
                ghosts.splice(i,1)
                score += 50
            }
            
        }
    
        ghosts.forEach( (ghost) => {
            ghost.update()
    
            const collisions = [ ]
    
            boundaries.forEach((boundary) => {
    
                if ( 
                    !collisions.includes('up') &&
                    collisionDetection( {circle: {...ghost, velocity: {x:0,y:-ghost.speed} } , rectangle: boundary} ) 
                    ){
    
                    collisions.push('up')
                }
    
                if ( 
                    !collisions.includes('down') &&
                    collisionDetection( {circle: {...ghost, velocity: {x:0,y:ghost.speed} } , rectangle: boundary} ) 
                    ){
    
                    collisions.push('down')
                }
    
                if ( 
                    !collisions.includes('left') &&
                    collisionDetection( {circle: {...ghost, velocity: {x:-ghost.speed,y:0} } , rectangle: boundary} )
                    ){
    
                    collisions.push('left')
                }
    
                if ( 
                    !collisions.includes('right') &&
                    collisionDetection( {circle: {...ghost, velocity: {x:ghost.speed,y:0} } , rectangle: boundary} )
                    ){
    
                    collisions.push('right')
                }
    
            })
    
            if (collisions.length > ghost.prevCollision.length){
                ghost.prevCollision = collisions
            }
            
            if (JSON.stringify(collisions) !== JSON.stringify(ghost.prevCollision)){
    
                if (ghost.velocity.x > 0){
                    ghost.prevCollision.push('right')
                }
    
                if (ghost.velocity.x < 0){
                    ghost.prevCollision.push('left')
                }
    
                if (ghost.velocity.y > 0){
                    ghost.prevCollision.push('down')
                }
    
                if (ghost.velocity.y < 0){
                    ghost.prevCollision.push('up')
                }
    
                const pathways = ghost.prevCollision.filter( (collision) => {
                    return !collisions.includes(collision)
                })
    
                const direction = pathways[ Math.floor(Math.random()*pathways.length) ]
    
                switch (direction){
                    
                    case 'up':
                        ghost.velocity.x = 0
                        ghost.velocity.y = -ghost.speed
                        break
    
                    case 'down':
                        ghost.velocity.x = 0
                        ghost.velocity.y = ghost.speed
                        break
    
                    case 'left':
                        ghost.velocity.x = -ghost.speed
                        ghost.velocity.y = 0
                        break
    
                    case 'right':
                        ghost.velocity.x = ghost.speed
                        ghost.velocity.y = 0
                        break
    
                }
    
                ghost.prevCollision = []
            }
    
            if (Math.hypot(ghost.position.x - player.position.x,ghost.position.y - player.position.y) < ghost.radius+player.radius && !ghost.scared){
                cancelAnimationFrame(animationId)
                winElem.textContent = 'Game Over'
                result.style.visibility = "visible"
                scoreNum.textContent = score
                restartBtn.style.pointerEvents = 'all'
            }
            
        })
    
        player.update()
    
        if (player.velocity.x > 0){
            player.rotation = 0
        }else if (player.velocity.x < 0){
            player.rotation = Math.PI
        }else if (player.velocity.y < 0){
            player.rotation = Math.PI * 1.5
        }else if (player.velocity.y > 0){
            player.rotation = Math.PI / 2
        }
    
    }
    
    animate()
    
    addEventListener('keydown',({key}) => {
    
        switch (key){
    
            case 'ArrowUp':
                keys.ArrowUp.pressed = true
                lastKey = 'ArrowUp'
                break
    
            case 'ArrowDown':
                keys.ArrowDown.pressed = true
                lastKey = 'ArrowDown'
                break
    
            case 'ArrowLeft':
                keys.ArrowLeft.pressed = true
                lastKey = 'ArrowLeft'
                break
    
            case 'ArrowRight':
                keys.ArrowRight.pressed = true
                lastKey = 'ArrowRight'
                break
    
        }
    
    })
    
    addEventListener('keyup',({key}) => {
    
        switch (key){
    
            case 'ArrowUp':
                keys.ArrowUp.pressed = false
                break
    
            case 'ArrowDown':
                keys.ArrowDown.pressed = false
                break
    
            case 'ArrowLeft':
                keys.ArrowLeft.pressed = false
                break
    
            case 'ArrowRight':
                keys.ArrowRight.pressed = false
                break
    
        }
    
    }) 
    
    restartBtn.addEventListener('click', function(){
        location.reload()
        result.style.visibility = 'hidden'
        restartBtn.style.pointerEvents = 'none'
    })
    
})

