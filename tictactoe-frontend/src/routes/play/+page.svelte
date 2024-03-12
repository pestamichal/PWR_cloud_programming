<script lang="ts">
    import { slide } from 'svelte/transition';

    let username = '';
    let game = false;
    let gameBoard = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']];
    let noConnectionErr = false;
    let invalidUsernameErr = false;
    let sessionId = '';

    const url = 'http://127.0.0.1:8000/api/register_for_game/';

    

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
                localStorage.setItem('session_id', sessionId);
            }else{
                noConnectionErr = true;
            }
        }catch(e){
            console.log(e);
            noConnectionErr = true;
        }
    }

    function makeMove(x: Number, y: Number) {
        console.log(x + " " + y);
    }

    function cancelGame(){
        sessionId = '';
        localStorage.setItem('session_id', '');
    }

    function endGame(){
        username = '';
        game = false;
    }
</script>


<div class=" flex flex-col justify-center items-center h-screen">
    <div class=" flex flex-col justify-center items-center bg-gray-200 px-10 py-16 gap-5 text-xl rounded-lg">
        {#if username && sessionId !== '' && game}
        <h1 class=" text-3xl font-bold">Tic Tac Toe</h1>
        <table class=" mx-5 my-auto">
            {#each gameBoard as row, i}
            <tr>
                {#each row as column, j}
                    <td class=" w-[100px] h-[100px] border-black border-2">
                        <button class=" h-full w-full text-6xl"
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
        <button 
            class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold"
            on:click={endGame}
        >
            End game
        </button>
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
    
</div>



