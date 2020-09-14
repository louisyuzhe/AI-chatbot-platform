<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
    <meta name="viewport"
      content="width=device-width, initial-scale=1.0, shrink-to-fit=no" />
    <link href="https://fonts.googleapis.com/css?family=Fira+Sans:400,400i,700&display=swap&subset=latin-ext" rel="stylesheet">
    <link rel="stylesheet" type="text/css" href="/blog/static/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="/blog/static/css/style.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.0.13/css/all.css" integrity="sha384-DNOHZ68U8hZfKXOrtjWvjxusGo9WQnrNx2sqG0tfsghAvtVlRW3tvkXWZh58N9jp" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>

  </head>
  <body>
    <header id="mainmenu-header">
    </header>
    <main>
      <div id="app" class="container top-padding">
      	<div class="row">
      		<div class="col-md-12">
      			<div class="card col-md-6" v-for="message in messages" v-bind:class="{ 'user-message': message.user,  'chat-message': message.chat_bot, 'offset-md-6': message.chat_bot}">
    	  			<div class="card-body">
    	  				[[message.text]]
    	  			</div>
    	  		</div>
      		</div>

      	</div>
      	<div id="text-box" class="row top-padding">
      		<div class="col-md-12">
      			<textarea class="form-control" v-bind:placeholder="placeholder" v-model="input" v-bind:class="{ 'border-danger': send_blank}" v-on:change="check_content"></textarea>
      			<i class="fas fa-arrow-circle-right send-btn" v-on:click="add_message"></i>
      		</div>
      	</div>
      </div>
    </main>
    <footer>
      <small>Site content and design by Yuzhe Lim</small>
    </footer>
  </body>
</html>

<script type="text/javascript">
  window.onload = function () {
    var app = new Vue({
      delimiters: ['[[', ']]'],
      el: '#app',
      data: {
        messages: [],
        input: '',
        send_blank: false,
        placeholder: 'Send a message to the chatbot...',
      },
      created: function() {

      },
      methods: {
      add_message: function() {
        if (this.input.length > 0) {
          var message = {
            'text': this.input,
            'user': true,
            'chat_bot': false,
          };
          this.messages.push(message);
          this.input = '';

          //just incase
          this.send_blank = false;
          this.placeholder = "Send a message to the chatbot...";

          fetch("/get-response/", {
                body: JSON.stringify({'message': message['text']}),
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                  'user-agent': 'Mozilla/4.0 MDN Example',
                  'content-type': 'application/json'
                },
                method: 'POST',
                mode: 'cors',
                redirect: 'follow',
                referrer: 'no-referrer',
                })
                .then(response => response.json()).then((json) => {
                    this.messages.push(json['message'])
              })
        } else {
          this.send_blank = true;
          this.placeholder = "Please put in some text";
        }

      },
      check_content: function() {
        if (this.input.length > 0) {
          this.send_blank = false;
          this.placeholder = "Send a message to the chatbot...";
        } else {
          this.send_blank = true;
          this.placeholder = "Please put in some text";
        }
      },
      }
    });
  };
</script>
