<html>                                                                  
 <head>                                                                  
 <title>Predicting users' interests</title>
 <script type="text/javascript" src="static/jquery.js"></script>          
 <link rel="stylesheet" href="static/bootstrap.min.css" type="text/css" media="screen">
 <link rel="stylesheet" href="static/olaii.css" type="text/css" media="screen">
<script src="static/bootstrap.js" type="text/javascript" charset="utf-8"></script>
 <script type="text/javascript">                                         
 </script>                                                               
 </head>                                                                 
 <body>                                                                  
      <div class="navbar navbar-inverse navbar-fixed-top">
      <div class="navbar-inner">
        <div class="container">
          <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <div class="nav-collapse collapse">
            <ul class="nav">
              <li class="active"><a href="#">Home</a></li>
              <li><a href="#about">About</a></li>
              <li><a href="#contact">Contact</a></li>
            </ul>
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>

    <div class="container">
	  <br><br>
      <h1>Predicting users' interests</h1>
      
      <form name="pform">
	  <fieldset>
	    <legend>Predict categories for user</legend>
	  <br>
	    <label>Twitter user name</label>
	    <input type="text" name="user_name">
		<br>
	    <input type="button" value="Predict" onclick="predict()"/>
	  </fieldset>
	  <br>
	  <div class="alert alert-success">
  			<button type="button" class="close" data-dismiss="alert">&times;</button>
  			<span id="predict-data">{{predict_msg}}</span>
  	  </div>
	</form>
      
      
      <form name="mform">
	  <fieldset>
	    <legend>Add category name and representing Twitter user</legend>
	  <br>
	    <label>Category name</label>
	    <input type="text" name="category" placeholder="programming" id="category">
	    <label>User name</label>
	    <input type="text" name="user" placeholder="JohnDCook" id="repr_user">
		<br>
	    <input type="button" value="Add category" onclick="add()"/>
		<br><br>	    
	    <div class="alert">
  			<button type="button" class="close" data-dismiss="alert">&times;</button>
  			<span id="output-data">{{data_time_msg}}</span>
		</div>
	  </fieldset>
	</form>
	  
	 <br><br> 
	 <table class="table">
	 <tr>
	   <th>Category</th>  
	   <th>Number of users</th>  
	   <th>Top keywords</th>  
	 </tr>
	 %for cat in categories:
  		<tr>
    		<td>{{cat[0]}}</td>
    		<td>{{cat[1]}}</td>
    		<td>{{top_keywords[cat[0]]}}</td>
  		</tr>
	 %end 
	</table>
	  
	  <br>
      <form name="tform">
	  <fieldset>
	    <legend>Train on collected data</legend>
	  <br>
	    <label>Train machine learning algorithm on registered categories</label>
	    <input type="button" value="Train" onclick="train()"/>
	    <br>
	    <br>
	    <div class="alert">
  			<button type="button" class="close" data-dismiss="alert">&times;</button>
  			<span id="output">{{time_msg}}</span>
		</div>
	  </fieldset>
	    
	</form>

    </div> <!-- /container -->
<script>
function predict(){
	uname=document.pform.user_name.value;
	 $("body").css("cursor", "progress");
	 $.ajax({ 
             type: "GET",
             dataType: "json",
             url: "http://" + "{{web_domain}}" + ":" + "{{web_port}}" + "/predict___" + uname,
             success: function(data){        
                $("#predict-data").text(data);
                $("body").css("cursor", "default");
             }
         });
      }

function add(){
	 cat = $("#category").val(); 
	 user = $("#repr_user").val(); 
	 $("body").css("cursor", "progress");
	 $.ajax({ 
             type: "GET",
             dataType: "json",
             url: "http://" + "{{web_domain}}" + ":" + "{{web_port}}" + "/addcat___" + cat + "___" + user,
             success: function(data){        
                $("#output-data").text(data);
                $("body").css("cursor", "default");
             }
         });
      }
      
function train(){
	 $("body").css("cursor", "progress");
	 $.ajax({ 
             type: "GET",
             dataType: "json",
             url: "http://" + "{{web_domain}}" + ":" + "{{web_port}}" + "/train",
             success: function(data){        
                $("#output").text(data);
                $("body").css("cursor", "default");
             }
         });
      }


</script>
  
 </body>                                                                 
 </html>
