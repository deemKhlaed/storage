function addIngredients(){
    $('#addIngredients').modal('show')
}


function logout() {
    if (confirm("Are you sure you want to logout? ")) {
        $.ajax({
       headers: 
       { "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content") },
       url: window.location.origin +'/logout/',
       type:'POST',
       
       success: function(response) {
       window.location.href = '/login'; 
       alert('loguot successfully!');
       
                           },
       error: function(xhr, errmsg, err) {
       alert('Falid to logout');
       }
       });
       }
   }

   function deleterecipe(id) {
    if (confirm("Are you sure you want to delete the recipe")) {
        $.ajax({
       headers: 
       { "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content") },
       url: '/deleteR/',
       type: 'POST',
       data:{id:id},
      
       success: function(response) {
       alert('Recipe deleted successfully!');

                           },
       error: function(xhr, errmsg, err) {
       alert('An error occurred while deleting the Recipe.');
       }
       });
       }
   }

   function editdatarecipe(id)
{
   
    var ajaxurl="/editR/"
    var id1 =document.getElementById("id1")
    var name =document.getElementById("Recipe_name")
    var description =document.getElementById("Recipe_description")


   $.ajax({
    headers: { "X-CSRF-TOKEN": $('meta[name="csrf-token"]').attr("content") },
    url:ajaxurl,
    data:{id:id},
    method:"POST",

    success:function(response){
        id1.value=response.value.id
        name.value= response.value.RecipesName
        description.value=response.value.description   
    }
   });


    $('#edit').modal('show')
}

   