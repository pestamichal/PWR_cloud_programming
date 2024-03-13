<script lang="ts">
    import { slide } from 'svelte/transition';
    import { onMount } from 'svelte';

    let username = '';
    let game = false;
    let gameBoard = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
    let noConnectionErr = false;
    let invalidUsernameErr = false;
    let sessionId = '';
    let playerType = ' ';
    let resultMessage = '';

    const url = 'http://127.0.0.1:8000/api/register_for_game/';
    let sessionSocket: WebSocket;
  

    onMount(async () => {
        const savedSessionId = sessionStorage.getItem('session_id');
        const savedUsername = sessionStorage.getItem('tictactoe_username');
        const savedPlayerType = sessionStorage.getItem('player_type');
        if(savedSessionId != null && savedUsername != null && savedPlayerType != null) {
            sessionId = savedSessionId;
            username = savedUsername;
            playerType = savedPlayerType;
        }else {
            sessionId = ''
        }

        sessionSocket = new WebSocket('ws://localhost:8000/ws/gamesession/');
        sessionSocket.onopen = function(e){
            if(sessionId !== '')
            sessionSocket.send(JSON.stringify({
                'type': 'init',
                'session_id': sessionId
            }))
        }
        sessionSocket.onmessage = function(e){
            const data = JSON.parse(e.data);
            const message_type = data['type'];
            const message_session_id = data['session_id'];
            if(message_session_id !== sessionId) return;
            switch(message_type){
                case 'init':
                    const gameActive = data['is_active'];
                    const playersReady = data['players_ready'];
                    gameBoard = data['board_state'];
                    if(gameActive && playersReady){
                        game = true;
                    }else if(gameActive){
                        game = false;
                    }else{
                        reset();
                    }
                    break;
                case 'begin_game': 
                    game = true;
                    break;
                case 'move': 
                    gameBoard = data['board_state'];
                    break;
                case 'result':
                    const winner = data['winner'];
                    const draw = data['draw'];
                    const victor_symbol = data['player_type'];
                    if(winner && victor_symbol === playerType){
                        resultMessage = 'You Won! :)'
                    }else if(winner && victor_symbol !== playerType){
                        resultMessage = 'You Lost... :('
                    }else if(draw){
                        resultMessage = 'Draw :|'
                    }
                    break;    
                case 'cancel': 
                    reset();
                    break;
                case 'gamenotfound':
                    reset();
                    break;
            }     
        }
        sessionSocket.onclose = function(e){
            console.error('Socket closed unexpectedly');
        }

    })

    async function handlePlay(){
        try{
            if(username === '') {
                invalidUsernameErr = true;
                return;
            };
            invalidUsernameErr = false;
            const response = await fetch(url + username + '/', {method: 'POST'});
            const data = await response.json();
            if(response.ok){    
                noConnectionErr = false;
                sessionId = data['session_id'];
                playerType = data['player_type'];
                sessionStorage.setItem('tictactoe_username', username);
                sessionStorage.setItem('session_id', sessionId);
                sessionStorage.setItem('player_type', playerType);
                sessionSocket.send(JSON.stringify({
                    'type': 'joined',
                    'session_id': sessionId
                }))
            }else{
                noConnectionErr = true;
            }
        }catch(e){
            console.error(e);
            noConnectionErr = true;
        }
    }

    function makeMove(x: Number, y: Number) {
        sessionSocket.send(JSON.stringify({
            'type': 'move',
            'session_id': sessionId,
            'row': x,
            'col': y,
            'player_type': playerType
        }))
    }

    function playAgain(){
        gameBoard = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
        game = false;
        resultMessage = '';
        if(playerType === 'X') playerType = 'O'
        else playerType = 'X';
        sessionSocket.send(JSON.stringify({
            'type': 'playagain',
            'session_id': sessionId
        }));
    }

    function cancelGame(){
        try{
            sessionSocket.send(JSON.stringify({
                'type': 'cancel',
                'session_id': sessionId,
            }))

        }catch(e){
            console.error(e);
        }
        reset();
    }

    function reset(){
        sessionId = '';
        playerType = '';
        game = false;
        resultMessage = '';
        gameBoard = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
        sessionStorage.setItem('session_id', sessionId);
        sessionStorage.setItem('player_type', playerType);
    }

</script>


<div class=" flex flex-col justify-center items-center h-screen gap-3">
    <div class=" flex flex-col justify-center items-center bg-gray-200 px-10 py-16 gap-5 text-xl rounded-lg">
        {#if username && sessionId !== '' && game}
        <h1 class=" text-3xl font-bold">Tic Tac Toe</h1>
        <table class=" mx-5 my-auto">
            {#each gameBoard as row, i}
            <tr>
                {#each row as column, j}
                    <td class=" w-[100px] h-[100px] border-black border-2">
                        <button class=" h-full w-full text-6xl {playerType == column ? 'text-green-500' : 'text-red-500'}"
                                on:click={() => {
                                   makeMove(i, j);
                                }}
                        >
                            {column}
                        </button>
                    </td>
                {/each}
                
            </tr>
            {/each}
        </table>
        {#if resultMessage === ''}
        <button 
            class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold"
            on:click={cancelGame}
        >
            End game
        </button>
        {:else}
        <button 
            class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold"
            on:click={playAgain}
        >
            Play Again!
        </button>  
        {/if}
        
        {:else if username && sessionId !== ''}
            <h1 class=" font-bold">Waiting for the other player...</h1>
            <i class="fa-solid fa-spinner fa-spin font-bold text-3xl"></i>
            <button 
                class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold"
                on:click={cancelGame}
            >
                Cancel Game
            </button>
        {:else}
            <h1 class=" font-bold">Chose your username</h1>
            <input class=" p-2 rounded-md"  type="text" placeholder="Username" bind:value={username}>
            <button class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold" on:click={handlePlay}>Play!</button>
            {#if invalidUsernameErr}
                <h1 transition:slide={{delay: 0, duration: 300}} class=" text-red-400">Invalid Username!</h1>
            {:else if noConnectionErr}
                <h1 transition:slide={{delay: 0, duration: 300}}>Can't connect to the server.</h1>
            {/if}
        {/if}
    </div>

    <h1 class=" font-bold text-3xl">{resultMessage}</h1>
    
</div>



