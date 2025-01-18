document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript is connected!");

    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('input', calculateTotals);
    });
    
    function calculateTotals() {
        let totalToClaim = 0;
    
        document.querySelectorAll('.total-to-claim').forEach(cell => {
            let row = cell.parentElement;
            let total = 0;
    
            row.querySelectorAll('input[type="number"]').forEach(input => {
                total += parseInt(input.value) || 0;
            });
    
            totalToClaim = total; // update total to claim for this row
            cell.textContent = totalToClaim;
        });
    }

    function getMealCountFromDOM() {
        const mealInputs = document.querySelectorAll('input[name="meal_count[]"]'); // Assuming meal counts are in input fields
        const mealCount = Array.from(mealInputs).reduce((total, input) => total + (parseInt(input.value) || 0), 0);
        console.log("Total Meal Count:", mealCount);
        return mealCount;
    }

    function getOperatingCost() {
        const receiptInputs = document.querySelectorAll('input[name="purchase_cost[]"]'); // Assuming costs are in input fields
        const operatingCost = Array.from(receiptInputs).reduce((total, input) => total + (parseFloat(input.value) || 0), 0);
        console.log("Total Operating Cost:", operatingCost);
        return operatingCost;
    }    

    // Function to show roster data in a modal (for other uses, if needed)
    function show_roster() {
        console.log("Roster Button Clicked");

        const modal = document.createElement("div");
        modal.id = "roster-modal";
        modal.style.position = "fixed";
        modal.style.top = "50%";
        modal.style.left = "50%";
        modal.style.transform = "translate(-50%, -50%)";
        modal.style.backgroundColor = "#fff";
        modal.style.padding = "20px";
        modal.style.boxShadow = "0 0 10px rgba(0,0,0,0.5)";
        modal.innerHTML = "<h3>Roster</h3><p>Fetching roster data...</p>";
        document.body.appendChild(modal);

        // Fetch roster data when the modal is shown
        fetchRosterData(modal);
    }

    // Function to remove a child from the roster
    function removeChildFromRoster(childId) {
        if (!childId) {
            console.error("Child ID is required to remove from the roster.");
            return;
        }

        // Confirm with the user before proceeding
        const confirmRemoval = confirm("Are you sure you want to remove this child from the roster?");
        if (!confirmRemoval) {
            return; // User canceled the removal
        }

        fetch(`/roster/remove-child/${childId}`, {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Failed to remove child with ID ${childId}`);
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                alert("Child removed successfully!");
                location.reload(); // Reload the page to reflect changes
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch((error) => {
            console.error("Error removing child:", error);
            alert("An error occurred while trying to remove the child.");
        });
    }

    // Fetch roster data and populate table
    function fetchRosterTable() {
        fetch("/roster/roster/get-roster", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("Fetched roster data:", data);

            const tableBody = document.getElementById("roster-table-body");
            if (!tableBody) {
                console.error("Roster table body not found in the DOM.");
                return;
            }

            // Clear existing rows
            tableBody.innerHTML = "";

            // Populate table rows with roster data
            data.forEach((child, index) => {
                const row = document.createElement("tr");
                row.innerHTML = `
                <td>${index + 1}</td>
                <td>${child.first_name}</td>
                <td>${child.last_name}</td>
                <td>${child.dob}</td>
                <td>${child.enrollment_date}</td>
                <td>${child.expiration_date}</td>
                <td><button class="remove-child" data-id="${child.id}">Remove</button></td>
            `;
                tableBody.appendChild(row);
            });

            // Add remove functionality
            document.querySelectorAll(".remove-child").forEach((button) => {
                button.addEventListener("click", (event) => {
                    const childId = event.target.dataset.id;
                    removeChildFromRoster(childId);
                });
            });
        })
        .catch((error) => {
            console.error("Error fetching roster data:", error);
            alert("Failed to fetch roster data.");
        });
    }

        
    // Add a child form dynamically
    const addChildButton = document.getElementById("add-child");
    const childrenContainer = document.getElementById("children-container");

    if (addChildButton) {
        addChildButton.addEventListener("click", () => {
            const childForm = document.createElement("div");
            childForm.classList.add("child-form");
            childForm.innerHTML = `
                <label>First Name: <input type="text" name="first_name[]" required></label>
                <label>Last Name: <input type="text" name="last_name[]" required></label>
                <label>Date of Birth: <input type="date" name="dob[]" required></label>
                <label>Enrollment Date: <input type="date" name="enrollment_date[]" required></label>
                <label>Expiration Date: <input type="date" name="expiration_date[]" required></label>
                <button type="button" class="remove-child">Remove</button>
            `;
            childrenContainer.appendChild(childForm);

            childForm.querySelector(".remove-child").addEventListener("click", () => {
                childForm.remove();
            });

            console.log("Added new child form.");
        });
    }


    // Submit enrollment data
    const submitButton = document.getElementById("submit-enroll");

    if (submitButton) {
        submitButton.addEventListener("click", async (event) => {
            event.preventDefault();
            console.log("Submit button clicked!");

            const firstNames = [];
            const lastNames = [];
            const dobs = [];
            const enrollmentDates = [];
            const expirationDates = [];

            document.querySelectorAll('input[name="first_name[]"]').forEach(input => firstNames.push(input.value));
            document.querySelectorAll('input[name="last_name[]"]').forEach(input => lastNames.push(input.value));
            document.querySelectorAll('input[name="dob[]"]').forEach(input => dobs.push(input.value));
            document.querySelectorAll('input[name="enrollment_date[]"]').forEach(input => enrollmentDates.push(input.value));
            document.querySelectorAll('input[name="expiration_date[]"]').forEach(input => expirationDates.push(input.value));

            const childrenData = [];
            for (let i = 0; i < firstNames.length; i++) {
                if (!firstNames[i] || !lastNames[i] || !dobs[i] || !enrollmentDates[i] || !expirationDates[i]) {
                    alert("Please fill all fields for each child.");
                    return;
                }

                childrenData.push({
                    first_name: firstNames[i],
                    last_name: lastNames[i],
                    dob: dobs[i],
                    enrollment_date: enrollmentDates[i],
                    expiration_date: expirationDates[i],
                });
            }

            console.log("Data being sent to the server:", JSON.stringify(childrenData));

            if (childrenData.length === 0) {
                alert("No data to submit. Please add children information.");
                return;
            }

            try {
                const response = await fetch("/enrollment/enrollment/submit-enroll", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(childrenData),
                });

                const data = await response.json();
                if (!response.ok) {
                    console.error("Server error:", data);
                    alert(`Error: ${data.error || "Failed to submit enrollments. Please try again."}`);
                    return;
                }

                alert("Enrollment successful!");
                window.location.reload();
            } catch (error) {
                console.error("Error submitting enrollments:", error);
                alert("Failed to submit enrollments. Please try again.");
            }
        });
    }

    // Function to dynamically create a claim form
    const addNewClaimButton = document.getElementById("create-claim");
    const claimsContainer = document.getElementById("claims-container");

    if (addNewClaimButton) {
        addNewClaimButton.addEventListener("click", () => {
            console.log("Create Claim button clicked!");
            window.location.href = "/claims/claims"; // Navigate to the claims page
        });

        // Create and append a claim form
        const claimForm = document.createElement("div");
        claimForm.innerHTML = `
            <h2>Create a New Claim</h2>
            <label>Total Operating Cost: <input type="number" name="operating_cost[]" required></label>
            <button type="button" class="add-receipt">Add Receipt</button>
            <div id="receipts-section"></div>
            <button type="button" class="submit-claim">Submit Claim</button>
            <button type="button" class="delete-claim">Cancel</button>
        `;
        claimsContainer.appendChild(claimForm);

        // Add functionality to "Add Receipt" button
        claimForm.querySelector(".add-receipt").addEventListener("click", () => {
            const receiptsSection = document.getElementById("receipts-section");
            const receiptDiv = document.createElement("div");
            receiptDiv.innerHTML = `
                <label>Date of Purchase: <input type="date" name="purchase_date[]" required></label>
                <label>Paid To: <input type="text" name="paid_to[]" required></label>
                <label>Type of Purchase:
                    <select name="purchase_type[]" required>
                        <option value="Food">Food</option>
                        <option value="Non-Food">Non-Food</option>
                        <option value="Food Services">Food Services</option>
                        <option value="Food Labor">Food Labor</option>
                        <option value="Milk (Whole/2%)">Milk (Whole/2%)</option>
                        <option value="Milk (Skim/1%)">Milk (Skim/1%)</option>
                    </select>
                </label>
                <button type="button" class="remove-receipt">Remove</button>
            `;
            receiptsSection.appendChild(receiptDiv);

            // Add remove functionality for receipt
            receiptDiv.querySelector(".remove-receipt").addEventListener("click", () => {
                receiptDiv.remove();
            });
        });

        // Handle form submission
        claimForm.querySelector(".submit-claim").addEventListener("click", async () => {
            const purchaseCost = document.querySelector('input[name="purchase_cost[]"]').value;
            const purchaseDates = Array.from(document.querySelectorAll('input[name="purchase_date[]"]')).map(el => el.value);
            const paidTo = Array.from(document.querySelectorAll('input[name="paid_to[]"]')).map(el => el.value);
            const purchaseTypes = Array.from(document.querySelectorAll('select[name="purchase_type[]"]')).map(el => el.value);
            const operatingCost = getOperatingCost('input[name="operating_cost[]"]').value;  // Calculate the total operating cost from the receipts
            const mealCount = await getMealCount('input[name="operating_cost[]"]').value;  // Fetch or calculate the total meal count
        

            const claimData = {
                purchase_cost: purchaseCost,
                paid_to: paidTo,
                purchase_type: purchaseTypes,
                purchase_date: purchaseDates,
                operating_cost: operatingCost,
                meal_counts: mealCount,
            };
            

            // Log the JSON data being sent
            console.log("JSON Data being sent:", JSON.stringify(claimData));

            try {
                const response = await fetch("/claims/claims/submit_claim", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(claimData),
                });

                // Handle response from the server
                const result = await response.json();
                if (response.ok) {
                    alert("Claim submitted successfully!");
                    claimsContainer.innerHTML = ""; // Clear the form
                } else {
                    console.error("Server Error Response:", result);
                    alert(`Error: ${result.error || result.message}`);
                }
            } catch (error) {
                console.error("Error submitting claim:", error);
                alert("An error occurred while submitting the claim. Please try again.");
            }
        });

        // Cancel claim creation
        claimForm.querySelector(".delete-claim").addEventListener("click", () => {
            claimsContainer.innerHTML = ""; // Clear the form
        });
    }
    

    // Function to fetch and display existing claims
    async function fetchClaims() {
        try {
            const response = await fetch("/get-claims", {
                method: "GET",
                headers: { "Content-Type": "application/json" }
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch claims data: ${response.statusText}`);
            }
            
            const data = await response.json();
        
            // Populate claims table
            const claimsTableBody = document.getElementById("claims-table-body");
            if (claimsTableBody) {
                claimsTableBody.innerHTML = "";
                data.claims.forEach((claim, index) => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${index + 1}</td>
                        <td>${claim.purchase_date}</td>
                        <td>${claim.paid_to}</td>
                        <td>${claim.purchase_type}</td>
                        <td>$${claim.purchase_cost.toFixed(2)}</td>
                    `;
                    claimsTableBody.appendChild(row);
                });
            }
        } catch (error) {
            console.error("Error fetching claims:", error);
        }
    }

    if (document.body.id === "claims-page") {
        // Fetch and display claims on page load
        fetchClaims();
    }

    // Load roster table on roster page
    if (document.body.id === "roster-page") {
        fetchRosterTable();
    }

    // View roster button
    const viewRosterButton = document.getElementById("view-roster-button");
    if (viewRosterButton) {
        viewRosterButton.addEventListener("click", () => {
            window.location.href = "/roster/roster";
        });
    }
});
