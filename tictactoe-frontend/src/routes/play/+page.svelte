<script lang="ts">
    let username = '';
    let game = false;
    let gameBoard = [[' ', ' ', ' '], [' ', ' ', 'X'], [' ', ' ', 'O']];

    function makeMove(x: Number, y: Number) {
        console.log(x + " " + y);
    }

    function endGame(){
        username = '';
        game = false;
    }
</script>


<div class=" flex flex-col justify-center items-center h-screen">
    <div class=" flex flex-col justify-center items-center bg-gray-200 px-10 py-16 gap-5 text-xl rounded-lg">
        {#if username && game}
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
        {:else}
            <h1 class=" font-bold">Chose your username</h1>
            <input class=" p-2 rounded-md"  type="text" placeholder="Username" bind:value={username}>
            <button class=" text-white bg-blue-500 px-3 py-2 rounded-md font-bold" on:click={() => {
                if(username !== ''){
                    game = true;
                }
            }}>Play!</button>
        {/if}
    </div>
    
</div>



