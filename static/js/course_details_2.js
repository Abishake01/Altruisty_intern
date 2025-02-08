

    function showLoading(event) {
        event.preventDefault();
    const button = event.target;


    button.classList.add('loading');


        setTimeout(() => {
        window.location.href = button.href;
        }, 1500); // Adjust the time as needed
    }
