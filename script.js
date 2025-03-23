document.addEventListener("DOMContentLoaded", function() {
    const pollForm = document.getElementById("pollForm");

    if (pollForm) {
        pollForm.addEventListener("submit", function(event) {
            event.preventDefault();
            const selectedOption = document.querySelector('input[name="vote"]:checked');

            if (selectedOption) {
                let votes = JSON.parse(localStorage.getItem("pollVotes")) || {};
                votes[selectedOption.value] = (votes[selectedOption.value] || 0) + 1;
                localStorage.setItem("pollVotes", JSON.stringify(votes));

                alert("Vote submitted successfully!");
                window.location.href = "results.html";  // Redirect to results page
            } else {
                alert("Please select an option before submitting.");
            }
        });
    }

    if (document.getElementById("pollChart")) {
        let votes = JSON.parse(localStorage.getItem("pollVotes")) || {};
        const labels = Object.keys(votes);
        const data = Object.values(votes);

        const ctx = document.getElementById("pollChart").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Votes",
                    data: data,
                    backgroundColor: ["#ff6384", "#36a2eb", "#ffce56", "#4bc0c0"],
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
});