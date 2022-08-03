document.getElementById('connect-button').addEventListener('click', event => {
  let account;
  ethereum.request({method: 'eth_requestAccounts'}).then(accounts => {
    account = accounts[0];
    console.log(account);

  });
});

ethereum.request({method: 'eth_getBalance' , params: [account, 'latest']}).then(result => {
  console.log(result);

});


let wei = parseInt(result,16); 
let balance = wei / (10**18);
console.log(balance + " ETH");

document.getElementById('connect-button').addEventListener('click', event => {
   let account;
   let button = event.target;
   ethereum.request({method: 'eth_requestAccounts'}).then(accounts => {
     account = accounts[0];
     console.log(account);
     button.textContent = account;
   });
...
 });