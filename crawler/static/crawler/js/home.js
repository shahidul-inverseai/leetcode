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

  for (const contest of myContext.contests) {
    const tableHeader = document.getElementsByClassName(contest.titleSlug)[0];
    const contestTitle = tableHeader.children[0].children[0];
    const refresh = tableHeader.children[0].children[1];
    const contestStatus = tableHeader.children[1].children[0];
    const contestTime = tableHeader.children[1].children[1];

    contestTitle.innerHTML = contest.title;

    if (contest["hasVirtualEnded"]) {
      tableHeader.classList.remove("running");
      tableHeader.className += " ended";
      refresh.innerHTML = "button";
      contestStatus.innerHTML = "ended on";
      contestTime.innerHTML = "end time";
    } else {
      tableHeader.classList.remove("ended");
      tableHeader.className += " running";
      refresh.innerHTML = "no button";
      contestStatus.innerHTML = "running";
      contestTime.innerHTML = "remaining time";
    }
  }

  const table = document.getElementById("contest_table");
  const tableBody = document.createElement("tbody");
  for (const contestant of myContext.users) {
    const row = document.createElement("tr");
    const cell = document.createElement("td");
    const cellText = document.createTextNode(contestant.name);

    row.appendChild(cell.appendChild(cellText));

    for (const contest of contestant.contests) {
      const divCell = document.createElement("td");
      const wrapperDiv = document.createElement("div");

      for (const soln of contest.hasSolved) {
        const innerDiv = document.createElement("div");
        // const button = document.createElement("button");
        const i_button = document.createElement("i");

        if (soln == "yes") {
          innerDiv.className = "accepted";
          i_button.className = "fas fa-check-circle";
        } else {
          innerDiv.className = "rejected";
          i_button.className = "fas fa-times-circle";
        }

        // button.appendChild(i_buttn);
        innerDiv.appendChild(i_button)
        wrapperDiv.appendChild(innerDiv)
      }
      divCell.appendChild(wrapperDiv)
      row.appendChild(divCell)
    }

    tableBody.appendChild(row);
  }
  console.log(table);
  table.appendChild(tableBody);
});

// const myContext = {{jsonContext|safe}};

//         for (let contest of myContext.contests) {

//         }
//       });

// let del_btn = document.createElement("button");
// let rot_btn = document.createElement("button");
// let i_del_btn = document.createElement("i");
// let i_rot_btn = document.createElement("i");
// i_del_btn.className = "fas fa-minus-circle";
// i_rot_btn.className = "fas fa-undo";
// del_btn.appendChild(i_del_btn);
// rot_btn.appendChild(i_rot_btn);
