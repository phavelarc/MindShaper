(function(win, doc){
  'use strict';

  //Verifica se o usuário realmente que deletar o dado
  if(doc.querySelectorAll('.btnDel')){
    let btnDel = doc.querySelectorAll('.btnDel');
    for(let i = 0; i < btnDel.length; i++){
      btnDel[i].addEventListener('click', function(e){
        if(confirm('Deseja mesmo apagar este livro?')){
          return true;
        } else {
          e.preventDefault();
        }
      });
    }
  }

  //Ajax do form
  if(doc.querySelectorAll('#form')){
    let form = doc.querySelector('#form');

    const sendForm = (e) => {
      e.preventDefault();
      let data = new FormData(form);
      let ajax = new XMLHttpRequest();
      let token = doc.querySelectorAll('input')
      ajax.open('POST', form.action);
      ajax.setRequestHeader('X-CSRF-TOKEN', token)
      ajax.onreadystatechange = function() {
        if(ajax.status === 200 && ajax.readyState === 4){
          console.log('Cadastrou!');
          let result = doc.querySelector('#result');
          result.innerHTML = 'Operação realizada com sucesso!'
          result.classList.add('alert');
          result.classList.add('alert-success');
          window.location = "/dashboard";
        }
      }
      ajax.send(data);
      form.reset();
    }
    form.addEventListener('submit', sendForm, false);
  }
})(window, document);