        <div class="panel p-1" id="container" >
            <h1 class="text-lg font-semibold dark:text-white-light p-1"
                style="background-color: rgb(138, 202, 167); border-radius: 9px;"><b>Family Details</b></h1>
                <div></div>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
                <div class="p-1">
                    <label class="p-1">Family-Member Name</label>
                    <input type="text" name="member_name" placeholder="Family-Member Name" class="form-input">
                </div>
                <div class="p-1">
                    <label class="p-1">Family-Member Age</label>
                    <input type="age" name="member_age" placeholder="Family-Member Age" class="form-input">
                </div>
                <div class="p-1">
                    <label class="p-1">Family-Member Relationship</label>
                    <input type="text" name="member_relation" placeholder="Family-Member Relationship" class="form-input">
                </div>
                <div class="p-1">
                    <label class="p-1"></label>
                    <button class="btn btn-success text-lg font-semibold dark:text-white-light" type="button"
                     onclick="add_more_field()">Add More</button>
                </div>
            </div>
        </div>
<script>
    var i=2;
         function add_more_field() {
        var container = document.getElementById("container");
        
        var newRow = document.createElement("div");
        
        newRow.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-4 gap-5 p-1">
            <div class="p-1"> 
                
               <input type="text" name="member_name`+i+`" placeholder="Family-Member Name" class="form-input">
            </div>
            <div class="p-1">
                <input type="age" name="member_age" placeholder="Family-Member Age" class="form-input">
            </div>
            <div class="p-1">
                <input type="text" name="member_relation" placeholder="Family-Member Relationship" class="form-input">
            </div>
            <button class="btn btn-danger text-lg font-semibold dark:text-white-light"style="padding: 10px 24px;" type="button" onclick="remove_field(this)">Close</button>
        </div>
        `;
        i++;
        
        container.appendChild(newRow);
    }
    function remove_field(button) {
        var row = button.parentNode;
        row.parentNode.removeChild(row);
        i--;
    }
  </script>