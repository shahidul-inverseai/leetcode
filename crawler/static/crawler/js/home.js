$(document).ready(function () {
  const myContext = JSON.parse(
    document.getElementById("myContext").textContent
  );

  $("#add-contest-btn").click(() => {
    $("#add-contest-btn").hide();
    $("#update-form").show();
  });

  $("#update-btn").click(() => {
    $("#update-form").hide();
    $("#add-contest-btn").show();
  });

  $("#cancel-btn").click(() => {
    $("#update-form").hide();
    $("#add-contest-btn").show();
  });

  // const table = document.getElementById("contest_table");
  // const tableBody = document.createElement("tbody");

  // for (const contest of myContext.contests) {
  //   const row = document.createElement("tr");
  //   const cell1 = document.createElement("td");
  //   const div1 = document.createElement("div");
  //   const anchor = document.createElement("a")
  //   const cellText1 = document.createTextNode(contest.title);

  //   const cell2 = document.createElement("td");
  //   const div2 = document.createElement("div");
  //   // const cellText2 = document.createTextNode(contest.);

  // }

  //   for (const contest of myContext.contests) {
  //     const tableHeader = document.getElementsByClassName(contest.titleSlug)[0];
  //     const contestTitle = tableHeader.children[0].children[0];
  //     const refresh = tableHeader.children[0].children[1];
  //     const contestStatus = tableHeader.children[1].children[0];
  //     const contestTime = tableHeader.children[1].children[1];

  //     contestTitle.innerHTML = contest.title;

  //     if (contest["hasVirtualEnded"]) {
  //       tableHeader.classList.remove("running");
  //       tableHeader.className += " ended";
  //       contestStatus.innerHTML = "ended on: " + contest.endTime;
  //     } else {
  //       tableHeader.classList.remove("ended");
  //       tableHeader.className += " running";
  //       const refresh_i_button = document.createElement("i");
  //       refresh_i_button.className = "fas fa-sync";
  //       refresh.appendChild(refresh_i_button);
  //       contestStatus.innerHTML = "remaining time: "+ contest.remainingTime;
  //     }
  //   }

  //   const table = document.getElementById("contest_table");
  //   const tableBody = document.createElement("tbody");
  //   for (const contestant of myContext.users) {
  //     const row = document.createElement("tr");
  //     const cell = document.createElement("td");
  //     const div = document.createElement("div");
  //     const cellText = document.createTextNode(contestant.name);

  //     div.appendChild(cellText);
  //     cell.appendChild(div);
  //     row.appendChild(cell);

  //     for (const contest of contestant.contests) {
  //       const divCell = document.createElement("td");
  //       const wrapperDiv = document.createElement("div");

  //       for (const soln of contest.hasSolved) {
  //         const innerDiv = document.createElement("div");
  //         // const button = document.createElement("button");
  //         const i_button = document.createElement("i");

  //         if (soln == "yes") {
  //           innerDiv.className = "accepted";
  //           i_button.className = "fas fa-check-circle";
  //         } else {
  //           innerDiv.className = "rejected";
  //           i_button.className = "fas fa-times-circle";
  //         }

  //         innerDiv.appendChild(i_button);
  //         wrapperDiv.appendChild(innerDiv);
  //       }
  //       divCell.appendChild(wrapperDiv);
  //       row.appendChild(divCell);
  //     }

  //     tableBody.appendChild(row);
  //   }
  //   table.appendChild(tableBody);
});
