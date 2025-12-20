const CodiCorrecteHash = "$2y$10$6fj0YCNzZQnQ3qyUJRsusuqAt6FJH.nNrF1R0xxTHnX62161z3yNC";

$(window).on("load",  async () => {

    $('#login').on("submit", async (event) => {
        event.preventDefault();
        try {
            var codi = $("#codi-acces");
            var bcrypt = dcodeIO.bcrypt;
            
            // Store password first
            sessionStorage.setItem("pass", codi.val());
            
            // Then verify
            if (bcrypt.compareSync(codi.val(), CodiCorrecteHash)) {
                // Password correct - redirect
                window.location.href = "graph.html";
            }
            else {
                // Password wrong - delete from storage and warn
                sessionStorage.removeItem("pass");
                alert("Codi incorrecte.");
            }
        } catch (error) {
            console.log(error);
            sessionStorage.removeItem("pass");
        }
    });
});