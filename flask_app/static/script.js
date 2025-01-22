document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript is connected!");
  
    document
      .querySelectorAll('input[type="number"]')
      .forEach((input) => {
        input.addEventListener("input", calculateTotals);
      });
  
    function calculateTotals() {
      let totalToClaim = 0;
  
      document.querySelectorAll(".total-to-claim").forEach((cell) => {
        let row = cell.parentElement;
        let total = 0;
  
        row.querySelectorAll('input[type="number"]').forEach((input) => {
          total += parseInt(input.value) || 0;
        });
  
        totalToClaim = total; // update total to claim for this row
        cell.textContent = totalToClaim;
      });
    }
  
    // Function to show roster data in a modal (for other uses, if needed)
    function showRoster() {
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
      const confirmRemoval = confirm(
        "Are you sure you want to remove this child from the roster?"
      );
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
    function fetchRosterData(modal) {
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
          document
            .querySelectorAll(".remove-child")
            .forEach((button) => {
              button.addEventListener("click", (event) => {
                const childId = event.target.dataset.id;
                removeChildFromRoster(childId);
              });
            });
        })
        .catch((error) => {
          console.error("Error fetching roster data:", error);
          alert("Failed to fetch roster data.");
        })
        .finally(() => {
          modal.remove();
        });
    }
  
    // Function to remove a child from the claims
    function removeClaimFromClaims(claimsId) {
      if (!claimsId) {
        console.error("Claims ID is required to remove from the claims.");
        return;
      }
  
      // Confirm with the user before proceeding
      const confirmRemoval = confirm(
        "Are you sure you want to remove this claim?"
      );
      if (!confirmRemoval) {
        return; // User canceled the removal
      }
  
      fetch(`/claims/remove-claims/${claimsId}`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`Failed to remove claim with ID ${claimsId}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("Claim removed successfully!");
            location.reload(); // Reload the page to reflect changes
          } else {
            alert(`Error: ${data.message}`);
          }
        })
        .catch((error) => {
          console.error("Error removing claim:", error);
          alert("An error occurred while trying to remove the claim.");
        });
    }
  
    // Fetch claim data and populate table
    function fetchClaimsData(modal) {
      fetch("/claims/claims/submit-claims", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
        })
        .then((response) => response.json())
        .then((data) => {
          console.log("Fetched claims data:", data);
  
          const tableBody = document.getElementById("claims-table-body");
          if (!tableBody) {
            console.error("Claims table body not found in the DOM.");
            return;
          }
  
          // Clear existing rows
          tableBody.innerHTML = "";
  
          // Populate table rows with claim data
          data.forEach((claims, index) => {
            const row = document.createElement("tr");
            row.innerHTML = `
              <td>${index + 1}</td>
              <td>${claims.purchase_type}</td>
              <td>${claims.purchase_cost}</td>
              <td>${claims.purchase_date}</td>
              <td>${claims.operating_cost}</td>
              <td>${claims.infant_breakfast_birth_3mo}</td>
              <td>${claims.infant_breakfast_4_7mos}</td>
              <td>${claims.infant_breakfast_8_12mos}</td>
              <td>${claims.child_breakfast_1yrs}</td>
              <td>${claims.child_breakfast_2yrs}</td>
              <td>${claims.child_breakfast_3_5yrs}</td>
              <td>${claims.child_breakfast_6_12yrs}</td>
              <td>${claims.infant_AMSnack_birth_3mo}</td>
              <td>${claims.infant_AMSnack_4_7mos}</td>
              <td>${claims.infant_AMSnack_8_12mos}</td>
              <td>${claims.child_AMSnack_1yrs}</td>
              <td>${claims.child_AMSnack_2yrs}</td>
              <td>${claims.child_AMSnack_3_5yrs}</td>
              <td>${claims.child_AMSnack_6_12yrs}</td>
              <td>${claims.infant_Lunch_birth_3mos}</td>
              <td>${claims.infant_Lunch_4_7mos}</td>
              <td>${claims.infant_Lunch_8_12mos}</td>
              <td>${claims.child_Lunch_1yrs}</td>
              <td>${claims.child_Lunch_2yrs}</td>
              <td>${claims.child_Lunch_3_5yrs}</td>                  
              <td>${claims.child_Lunch_6_12yrs}</td>                  
              <td>${claims.infant_PMSnack_birth_3mos}</td>
              <td>${claims.infant_PMSnack_4_7mos}</td>
              <td>${claims.infant_PMSnack_8_12mos}</td>
              <td>${claims.child_PMSnack_1yrs}</td>
              <td>${claims.child_PMSnack_2yrs}</td>
              <td>${claims.child_PMSnack_3_5yrs}</td>
              <td>${claims.child_PMSnack_6_12yrs}</td>
              <td>${claims.infant_Supper_birth_3mos}</td>
              <td>${claims.infant_Supper_4_7mos}</td>
              <td>${claims.infant_Supper_8_12mos}</td>
              <td>${claims.child_Supper_1yrs}</td>
              <td>${claims.child_Supper_2yrs}</td>
              <td>${claims.child_Supper_3_5yrs}</td>
              <td>${claims.child_Supper_6_12yrs}</td>
              <td><button class="remove-claims" data-id="${claims.id}">Remove</button></td>
            `;
            tableBody.appendChild(row);
          });
  
          // Add remove functionality
          document
            .querySelectorAll(".remove-claims")
            .forEach((button) => {
              button.addEventListener("click", (event) => {
                const claimsId = event.target.dataset.id;
                removeClaimFromClaims(claimsId);
              });
            });
        })
        .catch((error) => {
          console.error("Error fetching claim data:", error);
          alert("Failed to fetch claim data.");
        })
        .finally(() => {
          modal.remove();
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
          <label>Expiration Date: <input type="date" name="expiration_date[]"></label>
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
  
        const childrenData = Array.from(
          document.querySelectorAll(".child-form")
        ).map((form) => {
          const firstName = form.querySelector('input[name="first_name[]"]').value;
          const lastName = form.querySelector('input[name="last_name[]"]').value;
          const dob = form.querySelector('input[name="dob[]"]').value;
          const enrollmentDate = form.querySelector(
            'input[name="enrollment_date[]"]'
          ).value;
          const expirationDate = form.querySelector(
            'input[name="expiration_date[]"]'
          ).value;
  
          return {
            first_name: firstName,
            last_name: lastName,
            dob: dob,
            enrollment_date: enrollmentDate,
            expiration_date: expirationDate,
          };
        });
  
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
            alert(
              `Error: ${data.error || "Failed to submit enrollments. Please try again."}`
            );
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
        alert("Claim button clicked!");
        window.location.href = "/claims/claims"; // Navigate to the claims page
      });
    }
  });