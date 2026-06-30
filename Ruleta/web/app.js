let bankValue = 1000;
let currentBet = 0;
let wager = 5;
let lastWager = 0;
let bet = [];
let numbersBet = [];
let previousNumbers = [];

let numRed = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36];
let wheelnumbersAC = [0, 26, 3, 35, 12, 28, 7, 29, 18, 22, 9, 31, 14, 20, 1, 33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27, 6, 34, 17, 25, 2, 21, 4, 19, 15, 32];

let container = document.createElement('div');
container.setAttribute('id', 'container');
document.body.append(container);

//startGame();
let initialBankValue = 0;
let winsCount = 0;
let lossesCount = 0;

// Reemplaza el startGame() automático por este evento:
document.getElementById('btn-start').onclick = function() {
    let inputVal = parseInt(document.getElementById('start-balance').value);
    if(inputVal > 0) {
        initialBankValue = inputVal;
        bankValue = inputVal;
        document.getElementById('start-screen').style.display = 'none';
        startGame();
    } else {
        alert("Por favor, ingresa un monto válido mayor a 0.");
    }
};


let wheel = document.getElementsByClassName('wheel')[0];
let ballTrack = document.getElementsByClassName('ballTrack')[0];

function resetGame(){
    bankValue = 1000;
    currentBet = 0;
    wager = 5;
    bet = [];
    numbersBet = [];
    previousNumbers = [];
    document.getElementById('betting_board').remove();
    document.getElementById('notification').remove();
    buildBettingBoard();
}

/*function startGame(){
    buildWheel();
    buildBettingBoard();
}*/
function buildStatsPanel() {
    // Si la tabla ya existe, la borramos para evitar duplicados
    if (document.getElementById('stats-table')) {
        document.getElementById('stats-table').remove();
    }

    let table = document.createElement('table');
    table.setAttribute('id', 'stats-table');
    
    table.innerHTML = `
        <thead>
            <tr>
                <th>Rondas Ganadas</th>
                <th>Rondas Perdidas</th>
                <th>Balance Neto</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span id="stat-wins" class="ganancia">0</span></td>
                <td><span id="stat-losses" class="perdida">0</span></td>
                <td><span id="stat-net" class="neutro">$0</span></td>
            </tr>
        </tbody>
    `;
    
    // ¡LA CLAVE!: Lo añadimos al final de la página (fuera del juego)
    document.body.append(table);
}

function startGame(){
    buildWheel();
    buildBettingBoard();
    buildStatsPanel(); // <--- Llamamos al nuevo panel
}

function gameOver(){
    let notification = document.createElement('div');
    notification.setAttribute('id', 'notification');
    
    let nSpan = document.createElement('span');
    nSpan.setAttribute('class', 'nSpan');
    nSpan.innerText = 'Bancarrota';
    notification.append(nSpan);

    let nBtn = document.createElement('div');
    nBtn.setAttribute('class', 'nBtn');
    nBtn.innerText = 'Jugar de nuevo';   
    nBtn.onclick = function(){
        resetGame();
    };
    notification.append(nBtn);
    container.prepend(notification);
}

function buildWheel(){
    let wheel = document.createElement('div');
    wheel.setAttribute('class', 'wheel');

    let outerRim = document.createElement('div');
    outerRim.setAttribute('class', 'outerRim');
    wheel.append(outerRim);

    let numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26];
    for(let i = 0; i < numbers.length; i++){
        let a = i + 1;
        let spanClass = (numbers[i] < 10)? 'single' : 'double';
        let sect = document.createElement('div');
        sect.setAttribute('id', 'sect'+a);
        sect.setAttribute('class', 'sect');
        
        let span = document.createElement('span');
        span.setAttribute('class', spanClass);
        span.innerText = numbers[i];
        sect.append(span);
        
        let block = document.createElement('div');
        block.setAttribute('class', 'block');
        sect.append(block);
        wheel.append(sect);
    }

    let pocketsRim = document.createElement('div');
    pocketsRim.setAttribute('class', 'pocketsRim');
    wheel.append(pocketsRim);

    let ballTrack = document.createElement('div');
    ballTrack.setAttribute('class', 'ballTrack');
    let ball = document.createElement('div');
    ball.setAttribute('class', 'ball');
    ballTrack.append(ball);
    wheel.append(ballTrack);

    let pockets = document.createElement('div');
    pockets.setAttribute('class', 'pockets');
    wheel.append(pockets);

    let cone = document.createElement('div');
    cone.setAttribute('class', 'cone');
    wheel.append(cone);

    let turret = document.createElement('div');
    turret.setAttribute('class', 'turret');
    wheel.append(turret);

    let turretHandle = document.createElement('div');
    turretHandle.setAttribute('class', 'turretHandle');
    
    let thendOne = document.createElement('div');
    thendOne.setAttribute('class', 'thendOne');
    turretHandle.append(thendOne);
    
    let thendTwo = document.createElement('div');
    thendTwo.setAttribute('class', 'thendTwo');
    turretHandle.append(thendTwo);
    wheel.append(turretHandle);

    container.append(wheel);
}

function buildBettingBoard(){
    let bettingBoard = document.createElement('div');
    bettingBoard.setAttribute('id', 'betting_board');

    let wl = document.createElement('div');
    wl.setAttribute('class', 'winning_lines');
    
    var wlttb = document.createElement('div');
    wlttb.setAttribute('id', 'wlttb_top');
    wlttb.setAttribute('class', 'wlttb');
    
    for(let i = 0; i < 11; i++){
        let j = i;
        var ttbbetblock = document.createElement('div');
        ttbbetblock.setAttribute('class', 'ttbbetblock');
        var numA = (1 + (3 * j));
        var numB = (2 + (3 * j));
        var numC = (3 + (3 * j));
        var numD = (4 + (3 * j));
        var numE = (5 + (3 * j));
        var numF = (6 + (3 * j));
        let num = numA + ', ' + numB + ', ' + numC + ', ' + numD + ', ' + numE + ', ' + numF;
        var objType = 'double_street';
        
        ttbbetblock.onclick = function(){ setBet(this, num, objType, 5); };
        ttbbetblock.oncontextmenu = function(e){ e.preventDefault(); removeBet(this, num, objType, 5); };
        wlttb.append(ttbbetblock);
    }
    wl.append(wlttb);

    for(let c = 1; c < 4; c++){
        let d = c;
        var wlttb = document.createElement('div');
        wlttb.setAttribute('id', 'wlttb_'+c);
        wlttb.setAttribute('class', 'wlttb');
        for(let i = 0; i < 12; i++){
            let j = i;
            var ttbbetblock = document.createElement('div');
            ttbbetblock.setAttribute('class', 'ttbbetblock');
            ttbbetblock.onclick = function(){
                var numA, numB, numC, num;
                if(d == 1 || d == 2){
                    numA = ((2 - (d - 1)) + (3 * j));
                    numB = ((3 - (d - 1)) + (3 * j));
                    num = numA + ', ' + numB;
                } else{
                    numA = (1 + (3 * j));
                    numB = (2 + (3 * j));
                    numC = (3 + (3 * j));
                    num = numA + ', ' + numB + ', ' + numC;
                }
                var objType = (d == 3)? 'street' : 'split';
                var odd = (d == 3)? 11 : 17;
                setBet(this, num, objType, odd);
            };
            ttbbetblock.oncontextmenu = function(e){
                e.preventDefault();
                var numA, numB, numC, num;
                if(d == 1 || d == 2){
                    numA = ((2 - (d - 1)) + (3 * j));
                    numB = ((3 - (d - 1)) + (3 * j));
                    num = numA + ', ' + numB;
                } else{
                    numA = (1 + (3 * j));
                    numB = (2 + (3 * j));
                    numC = (3 + (3 * j));
                    num = numA + ', ' + numB + ', ' + numC;
                }
                var objType = (d == 3)? 'street' : 'split';
                var odd = (d == 3)? 11 : 17;
                removeBet(this, num, objType, odd);
            };
            wlttb.append(ttbbetblock);
        }
        wl.append(wlttb);
    }

    for(let c = 1; c < 12; c++){
        let d = c;
        var wlrtl = document.createElement('div');
        wlrtl.setAttribute('id', 'wlrtl_'+c);
        wlrtl.setAttribute('class', 'wlrtl');
        for(let i = 1; i < 4; i++){
            let j = i;
            var rtlbb = document.createElement('div');
            rtlbb.setAttribute('class', 'rtlbb'+i);
            var numA = (3 + (3 * (d - 1))) - (j - 1);
            var numB = (6 + (3 * (d - 1))) - (j - 1);
            let num = numA + ', ' + numB;
            rtlbb.onclick = function(){ setBet(this, num, 'split', 17); };
            rtlbb.oncontextmenu = function(e){ e.preventDefault(); removeBet(this, num, 'split', 17); };
            wlrtl.append(rtlbb);
        }
        wl.append(wlrtl);
    }
    
    for(let c = 1; c < 3; c++){
        var wlcb = document.createElement('div');
        wlcb.setAttribute('id', 'wlcb_'+c);
        wlcb.setAttribute('class', 'wlcb');
        for(let i = 1; i < 12; i++){
            let count = (c == 1)? i : i + 11;
            var cbbb = document.createElement('div');
            cbbb.setAttribute('id', 'cbbb_'+count);
            cbbb.setAttribute('class', 'cbbb');
            var numA = '2';
            var numB = '3';
            var numC = '5';
            var numD = '6';
            let num = (count >= 1 && count < 12)? (parseInt(numA) + ((count - 1) * 3)) + ', ' + (parseInt(numB)+((count - 1) * 3)) + ', ' + (parseInt(numC)+((count - 1) * 3)) + ', ' + (parseInt(numD)+((count - 1) * 3)) : ((parseInt(numA) - 1) + ((count - 12) * 3)) + ', ' + ((parseInt(numB) - 1)+((count - 12) * 3)) + ', ' + ((parseInt(numC) - 1)+((count - 12) * 3)) + ', ' + ((parseInt(numD) - 1)+((count - 12) * 3));
            var objType = 'corner_bet';
            
            cbbb.onclick = function(){ setBet(this, num, objType, 8); };
            cbbb.oncontextmenu = function(e){ e.preventDefault(); removeBet(this, num, objType, 8); };
            wlcb.append(cbbb);
        }
        wl.append(wlcb);
    }

    bettingBoard.append(wl);

    let bbtop = document.createElement('div');
    bbtop.setAttribute('class', 'bbtop');
    let bbtopBlocks = ['1 a 18', '19 a 36'];
    
    for(let i = 0; i < bbtopBlocks.length; i++){
        let f = i;
        var bbtoptwo = document.createElement('div');
        bbtoptwo.setAttribute('class', 'bbtoptwo');
        let num = (f == 0)? '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18' : '19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36';
        var objType = (f == 0)? 'outside_low' : 'outside_high';
        
        bbtoptwo.onclick = function(){ setBet(this, num, objType, 1); };
        bbtoptwo.oncontextmenu = function(e){ e.preventDefault(); removeBet(this, num, objType, 1); };
        bbtoptwo.innerText = bbtopBlocks[i];
        bbtop.append(bbtoptwo);
    }
    bettingBoard.append(bbtop);

    let numberBoard = document.createElement('div');
    numberBoard.setAttribute('class', 'number_board');

    let zero = document.createElement('div');
    zero.setAttribute('class', 'number_0');
    var objType = 'zero';
    var odds = 35;
    
    zero.onclick = function(){ setBet(this, '0', objType, odds); };
    zero.oncontextmenu = function(e){ e.preventDefault(); removeBet(this, '0', objType, odds); };
    
    let nbnz = document.createElement('div');
    nbnz.setAttribute('class', 'nbn');
    nbnz.innerText = '0';
    zero.append(nbnz);
    numberBoard.append(zero);
    
    var numberBlocks = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, '2 a 1', 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, '2 a 1', 1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34, '2 a 1'];
    var redBlocks = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36];
    
    for(let i = 0; i < numberBlocks.length; i++){
        let a = i;
        var nbClass = (numberBlocks[i] == '2 a 1')? 'tt1_block' : 'number_block';
        var colourClass = (redBlocks.includes(numberBlocks[i]))? ' redNum' : ((nbClass == 'number_block')? ' blackNum' : '');
        var numberBlock = document.createElement('div');
        numberBlock.setAttribute('class', nbClass + colourClass);
        
        numberBlock.onclick = function(){
            if(numberBlocks[a] != '2 a 1'){
                setBet(this, ''+numberBlocks[a]+'', 'inside_whole', 35);
            }else{
                let num = (a == 12)? '3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36' : ((a == 25)? '2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35' : '1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34');
                setBet(this, num, 'outside_column', 2);
            }
        };
        numberBlock.oncontextmenu = function(e){
            e.preventDefault();
            if(numberBlocks[a] != '2 a 1'){
                removeBet(this, ''+numberBlocks[a]+'', 'inside_whole', 35);
            }else{
                let num = (a == 12)? '3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36' : ((a == 25)? '2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35' : '1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34');
                removeBet(this, num, 'outside_column', 2);
            }
        };
        
        var nbn = document.createElement('div');
        nbn.setAttribute('class', 'nbn');
        nbn.innerText = numberBlocks[i];
        numberBlock.append(nbn);
        numberBoard.append(numberBlock);
    }
    bettingBoard.append(numberBoard);

    let bo3Board = document.createElement('div');
    bo3Board.setAttribute('class', 'bo3_board');    
    let bo3Blocks = ['1ra 12', '2da 12', '3ra 12'];
    
    for(let i = 0; i < bo3Blocks.length; i++){
        let b = i;
        var bo3Block = document.createElement('div');
        bo3Block.setAttribute('class', 'bo3_block');
        
        bo3Block.onclick = function(){
            let num = (b == 0)? '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12' : ((b == 1)? '13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24' : '25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36');
            setBet(this, num, 'outside_dozen', 2);
        };
        bo3Block.oncontextmenu = function(e){
            e.preventDefault();
            let num = (b == 0)? '1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12' : ((b == 1)? '13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24' : '25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36');
            removeBet(this, num, 'outside_dozen', 2);
        };
        bo3Block.innerText = bo3Blocks[i];
        bo3Board.append(bo3Block);
    }
    bettingBoard.append(bo3Board);

    let otoBoard = document.createElement('div');
    otoBoard.setAttribute('class', 'oto_board');    
    let otoBlocks = ['PAR', 'ROJO', 'NEGRO', 'IMPAR'];
    
    for(let i = 0; i < otoBlocks.length; i++){
        let d = i;
        var colourClass = (otoBlocks[i] == 'ROJO')? ' redNum' : ((otoBlocks[i] == 'NEGRO')? ' blackNum' : '');
        var otoBlock = document.createElement('div');
        otoBlock.setAttribute('class', 'oto_block' + colourClass);
        
        otoBlock.onclick = function(){
            let num = (d == 0)? '2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36' : ((d == 1)? '1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36' : ((d == 2)? '2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35' : '1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35'));
            setBet(this, num, 'outside_oerb', 1);
        };
        otoBlock.oncontextmenu = function(e){
            let num = (d == 0)? '2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36' : ((d == 1)? '1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36' : ((d == 2)? '2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35' : '1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35'));
            e.preventDefault();
            removeBet(this, num, 'outside_oerb', 1);
        };
        otoBlock.innerText = otoBlocks[i];
        otoBoard.append(otoBlock);
    }
    bettingBoard.append(otoBoard);

    let chipDeck = document.createElement('div');
    chipDeck.setAttribute('class', 'chipDeck');
    let chipValues = [1, 5, 10, 100, 'Limpiar'];
    
    for(let i = 0; i < chipValues.length; i++){
        let cvi = i;
        let chipColour = (i == 0)? 'red' : ((i == 1)? 'blue cdChipActive' : ((i == 2)? 'orange' : ((i == 3)? 'gold' : 'clearBet')));
        let chip = document.createElement('div');
        chip.setAttribute('class', 'cdChip ' + chipColour);
        
        chip.onclick = function(){
            if(cvi !== 4){
                let cdChipActive = document.getElementsByClassName('cdChipActive');
                for(let j = 0; j < cdChipActive.length; j++){
                    cdChipActive[j].classList.remove('cdChipActive');
                }
                let curClass = this.getAttribute('class');
                if(!curClass.includes('cdChipActive')){
                    this.setAttribute('class', curClass + ' cdChipActive');
                }
                wager = parseInt(chip.childNodes[0].innerText);
            }else{
                bankValue = bankValue + currentBet;
                currentBet = 0;
                document.getElementById('bankSpan').innerText = '$' + bankValue.toLocaleString("en-GB") + '';
                document.getElementById('betSpan').innerText = '$' + currentBet.toLocaleString("en-GB") + '';
                clearBet();
                removeChips();
            }
        };
        let chipSpan = document.createElement('span');
        chipSpan.setAttribute('class', 'cdChipSpan');
        chipSpan.innerText = chipValues[i];
        chip.append(chipSpan);
        chipDeck.append(chip);
    }
    bettingBoard.append(chipDeck);

    let bankContainer = document.createElement('div');
    bankContainer.setAttribute('class', 'bankContainer');

    let bank = document.createElement('div');
    bank.setAttribute('class', 'bank');
    let bankSpan = document.createElement('span');
    bankSpan.setAttribute('id', 'bankSpan');
    bankSpan.innerText = '$' + bankValue.toLocaleString("en-GB") + '';
    bank.append(bankSpan);
    bankContainer.append(bank);

    let betDisplay = document.createElement('div');
    betDisplay.setAttribute('class', 'bet');
    let betSpan = document.createElement('span');
    betSpan.setAttribute('id', 'betSpan');
    betSpan.innerText = '$' + currentBet.toLocaleString("en-GB") + '';
    betDisplay.append(betSpan);
    bankContainer.append(betDisplay);    
    
    bettingBoard.append(bankContainer);

    let pnBlock = document.createElement('div');
    pnBlock.setAttribute('class', 'pnBlock');
    let pnContent = document.createElement('div');
    pnContent.setAttribute('id', 'pnContent');
    pnContent.onwheel = function(e){
        e.preventDefault();
        pnContent.scrollLeft += e.deltaY;
    };
    pnBlock.append(pnContent);  
    bettingBoard.append(pnBlock);
    
    container.append(bettingBoard);
}

function clearBet(){
    bet = [];
    numbersBet = [];
}

function setBet(e, n, t, o){
    lastWager = wager;
    wager = (bankValue < wager)? bankValue : wager;
    if(wager > 0){
        if(!container.querySelector('.spinBtn')){
            let spinBtn = document.createElement('div');
            spinBtn.setAttribute('class', 'spinBtn');
            spinBtn.innerText = 'GIRAR';
            spinBtn.onclick = function(){
                this.remove();
                spin();
            };
            container.append(spinBtn);
        }
        bankValue = bankValue - wager;
        currentBet = currentBet + wager;
        document.getElementById('bankSpan').innerText = '$' + bankValue.toLocaleString("en-GB") + '';
        document.getElementById('betSpan').innerText = '$' + currentBet.toLocaleString("en-GB") + '';
        
        for(let i = 0; i < bet.length; i++){
            if(bet[i].numbers == n && bet[i].type == t){
                bet[i].amt = bet[i].amt + wager;
                let chipColour = (bet[i].amt < 5)? 'red' : ((bet[i].amt < 10)? 'blue' : ((bet[i].amt < 100)? 'orange' : 'gold'));
                e.querySelector('.chip').style.cssText = '';
                e.querySelector('.chip').setAttribute('class', 'chip ' + chipColour);
                let chipSpan = e.querySelector('.chipSpan');
                chipSpan.innerText = bet[i].amt;
                return;
            }
        }
        var obj = {
            amt: wager,
            type: t,
            odds: o,
            numbers: n
        };
        bet.push(obj);
        
        let numArray = n.split(',').map(Number);
        for(let i = 0; i < numArray.length; i++){
            if(!numbersBet.includes(numArray[i])){
                numbersBet.push(numArray[i]);
            }
        }

        if(!e.querySelector('.chip')){
            let chipColour = (wager < 5)? 'red' : ((wager < 10)? 'blue' : ((wager < 100)? 'orange' : 'gold'));
            let chip = document.createElement('div');
            chip.setAttribute('class', 'chip ' + chipColour);
            let chipSpan = document.createElement('span');
            chipSpan.setAttribute('class', 'chipSpan');
            chipSpan.innerText = wager;
            chip.append(chipSpan);
            e.append(chip);
        }
    }
}

function spin(){
    var winningSpin = Math.floor(Math.random() * 37);
    spinWheel(winningSpin);
    setTimeout(function(){
        if(numbersBet.includes(winningSpin)){
            /*let winValue = 0;
            let betTotal = 0;
            for(let i = 0; i < bet.length; i++){
                var numArray = bet[i].numbers.split(',').map(Number);
                if(numArray.includes(winningSpin)){
                    bankValue = (bankValue + (bet[i].odds * bet[i].amt) + bet[i].amt);
                    winValue = winValue + (bet[i].odds * bet[i].amt);
                    betTotal = betTotal + bet[i].amt;
                }
            }
            win(winningSpin, winValue, betTotal);*/
            let winValue = 0;
            let betTotal = 0;
            
            // Calcular dinero ganado y apostado
            if(numbersBet.includes(winningSpin)){
                for(let i = 0; i < bet.length; i++){
                    var numArray = bet[i].numbers.split(',').map(Number);
                    if(numArray.includes(winningSpin)){
                        bankValue = (bankValue + (bet[i].odds * bet[i].amt) + bet[i].amt);
                        winValue += (bet[i].odds * bet[i].amt);
                    }
                    betTotal += bet[i].amt; 
                }
                win(winningSpin, winValue, betTotal);
            } else {
                // Calcular lo que apostó si perdió
                for(let i = 0; i < bet.length; i++) betTotal += bet[i].amt;
            }

            // Actualizar Estadísticas DOM
            if(winValue > 0) winsCount++;
            else if (betTotal > 0) lossesCount++;
            
            let netProfit = bankValue - initialBankValue;
            document.getElementById('stat-wins').innerText = winsCount;
            document.getElementById('stat-losses').innerText = lossesCount;
            
            let statNet = document.getElementById('stat-net');
            if(netProfit > 0) {
                statNet.innerText = "+$" + netProfit; statNet.className = "ganancia";
            } else if (netProfit < 0) {
                statNet.innerText = "-$" + Math.abs(netProfit); statNet.className = "perdida";
            } else {
                statNet.innerText = "$0"; statNet.className = "neutro";
            }
        }

        currentBet = 0;
        document.getElementById('bankSpan').innerText = '$' + bankValue.toLocaleString("en-GB") + '';
        document.getElementById('betSpan').innerText = '$' + currentBet.toLocaleString("en-GB") + '';
        
        let pnClass = (numRed.includes(winningSpin))? 'pnRed' : ((winningSpin == 0)? 'pnGreen' : 'pnBlack');
        let pnContent = document.getElementById('pnContent');
        let pnSpan = document.createElement('span');
        pnSpan.setAttribute('class', pnClass);
        pnSpan.innerText = winningSpin;
        pnContent.append(pnSpan);
        pnContent.scrollLeft = pnContent.scrollWidth;

        bet = [];
        numbersBet = [];
        removeChips();
        wager = lastWager;
        if(bankValue == 0 && currentBet == 0){
            gameOver();
        }
    }, 10000);
}

function win(winningSpin, winValue, betTotal){
    if(winValue > 0){
        let notification = document.createElement('div');
        notification.setAttribute('id', 'notification');
        
        let nSpan = document.createElement('div');
        nSpan.setAttribute('class', 'nSpan');
        
        let nsnumber = document.createElement('span');
        nsnumber.setAttribute('class', 'nsnumber');
        nsnumber.style.cssText = (numRed.includes(winningSpin))? 'color:red' : 'color:black';
        nsnumber.innerText = winningSpin;
        nSpan.append(nsnumber);
        
        let nsTxt = document.createElement('span');
        nsTxt.innerText = ' Ganador';
        nSpan.append(nsTxt);
        
        let nsWin = document.createElement('div');
        nsWin.setAttribute('class', 'nsWin');
        
        let nsWinBlock = document.createElement('div');
        nsWinBlock.setAttribute('class', 'nsWinBlock');
        nsWinBlock.innerText = 'Apuesta: ' + betTotal;
        nsWin.append(nsWinBlock);
        
        nsWinBlock = document.createElement('div');
        nsWinBlock.setAttribute('class', 'nsWinBlock');
        nsWinBlock.innerText = 'Ganancia: ' + winValue;
        nsWin.append(nsWinBlock);
        
        nsWinBlock = document.createElement('div');
        nsWinBlock.setAttribute('class', 'nsWinBlock');
        nsWinBlock.innerText = 'Total: ' + (winValue + betTotal);
        nsWin.append(nsWinBlock);
        
        nSpan.append(nsWin);
        notification.append(nSpan);
        container.prepend(notification);
        
        setTimeout(function(){
            notification.style.cssText = 'opacity:0';
        }, 3000);
        setTimeout(function(){
            notification.remove();
        }, 4000);
    }
}

function removeBet(e, n, t, o){
    wager = (wager == 0)? 100 : wager;
    for(let i = 0; i < bet.length; i++){
        if(bet[i].numbers == n && bet[i].type == t){
            if(bet[i].amt != 0){
                wager = (bet[i].amt > wager)? wager : bet[i].amt;
                bet[i].amt = bet[i].amt - wager;
                bankValue = bankValue + wager;
                currentBet = currentBet - wager;
                document.getElementById('bankSpan').innerText = '$' + bankValue.toLocaleString("en-GB") + '';
                document.getElementById('betSpan').innerText = '$' + currentBet.toLocaleString("en-GB") + '';
                
                if(bet[i].amt == 0){
                    e.querySelector('.chip').style.cssText = 'display:none';
                }else{
                    let chipColour = (bet[i].amt < 5)? 'red' : ((bet[i].amt < 10)? 'blue' : ((bet[i].amt < 100)? 'orange' : 'gold'));
                    e.querySelector('.chip').setAttribute('class', 'chip ' + chipColour);
                    let chipSpan = e.querySelector('.chipSpan');
                    chipSpan.innerText = bet[i].amt;
                }
            }
        }
    }

    if(currentBet == 0 && container.querySelector('.spinBtn')){
        document.getElementsByClassName('spinBtn')[0].remove();
    }
}

function spinWheel(winningSpin){
    var degree = 0;
    for(let i = 0; i < wheelnumbersAC.length; i++){
        if(wheelnumbersAC[i] == winningSpin){
            degree = (i * 9.73) + 362;
        }
    }
    wheel.style.cssText = 'animation: wheelRotate 5s linear infinite;';
    ballTrack.style.cssText = 'animation: ballRotate 1s linear infinite;';

    setTimeout(function(){
        ballTrack.style.cssText = 'animation: ballRotate 2s linear infinite;';
        window.styleTag = document.createElement('style');
        window.styleTag.type = 'text/css';
        window.styleTag.innerText = '@keyframes ballStop {from {transform: rotate(0deg);}to{transform: rotate(-'+degree+'deg);}}';
        document.head.appendChild(window.styleTag);
    }, 2000);
    
    setTimeout(function(){
        ballTrack.style.cssText = 'animation: ballStop 3s linear;';
    }, 6000);
    
    setTimeout(function(){
        ballTrack.style.cssText = 'transform: rotate(-'+degree+'deg);';
    }, 9000);
    
    setTimeout(function(){
        wheel.style.cssText = '';
        if(window.styleTag) window.styleTag.remove();
    }, 10000);
}

function removeChips(){
    var chips = document.getElementsByClassName('chip');
    if(chips.length > 0){
        for(let i = 0; i < chips.length; i++){
            chips[i].remove();
        }
        removeChips();
    }
}



