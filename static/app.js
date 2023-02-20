// Define Global Variables
let potNames = [];
let potResp = [];
let spellNames = [];
let spellResp = [];

// Potions
const $potionContainer = $("#potion-results");
const $searchPotions = $("#search-potions");

$(document).ready(function () {
  getAllPotions();
});

// On document load it gets all potions from the API and then creates a list of the potion names
async function getAllPotions() {
  // gets all potions from the API
  resp = await axios.get("/potions/search");
  potResp = resp.data;

  for (let i = 0; i < potResp.length; i++) {
    potNames.push(potResp[i].name);
  }
}

//on key up searchs for potions by letter
$searchPotions.on("keyup", function (evt) {
  evt.preventDefault();
  const letter = evt.target.value;
  console.log(letter);
  if (letter == "") {
    return;
  } else {
    getMatchingPotions(letter);
  }
});

// On key press searches for matching names based on the letter input into the search bar
function getMatchingPotions(letter) {
  $potionContainer.empty();
  for (let i = 0; i < potNames.length; i++) {
    if (potNames[i].toUpperCase().startsWith(letter.toUpperCase())) {
      let $potion = generatePotionMarkup(potResp[i]);
      $potionContainer.append($potion);
    }
  }
  $potionContainer.show();
}

// generates HTML for putting potion on the page based on search
function generatePotionMarkup(potion) {
  return $(`
    <div class="col-sm-3">
        <div class="card box text-center">
            <a href="/potions/${potion.id}"><img class="card-img-top char-img img-fluid" src="${potion.image}"></a>
            <div class="card-body">
            <p class="card-text-center" style="font-size: .8rem">${potion.name}</p>
            </div>
        </div>
    </div>
`);
}

// Spells
const $searchSpells = $("#search-spells");
const $spellContainer = $("#spell-results");

$(document).ready(function () {
  getAllSpells();
});

// On document load it gets all spells from the API and then creates a list of the spell names
async function getAllSpells() {
  // gets all potions from the API
  resp = await axios.get("/spells/search");
  spellResp = resp.data;

  for (let i = 0; i < spellResp.length; i++) {
    spellNames.push(spellResp[i].name);
  }
}

//on key up searchs for spells by letter
$searchSpells.on("keyup", function (evt) {
  evt.preventDefault();
  const letter = evt.target.value;
  if (letter == "") {
    return;
  } else {
    getMatchingSpells(letter);
  }
});

// On key press searches for matching names based on the letter input into the search bar
function getMatchingSpells(letter) {
  $spellContainer.empty();
  for (let i = 0; i < spellNames.length; i++) {
    if (spellNames[i].toUpperCase().startsWith(letter.toUpperCase())) {
      let $spell = generateSpellMarkup(spellResp[i]);
      $spellContainer.append($spell);
    }
  }
  $spellContainer.show();
}

function generateSpellMarkup(spell) {
  return $(`
    <div class="col-sm-4 col-md-3 col-xl-2">
        <div class="card text-center">
            <a href="/spells/${spell.id}"><img class="card-img-top img-fluid" src="${spell.image}"></a>
            <div class="card-body">
            <p class="card-text-center" style="font-size: .8rem">${spell.name}</p>
            </div>
        </div>
    </div>
`);
}

// confirm the logout process
const $logoutBtn = $("#logout");
$logoutBtn.on("click", checkLogout);

function checkLogout(evt) {
  const $target = $(evt.target);
  $closestA = $target.closest("a");

  const response = confirm("Are you sure you want to logout?");
  if (response) {
    $closestA.prop("href", "/logout");
  }
}

// confirm delete account
const $deleteBtn = $("#del");
$deleteBtn.on("click", checkDelete);

function checkDelete(evt) {
  const $target = $(evt.target);
  $closestA = $target.closest("a");
  $closestLi = $target.closest("li");
  const userId = $closestLi[0].id;

  const response = confirm("Are you sure you want to delete your account?");
  if (response) {
    $closestA.prop("href", `/user/${userId}/delete`);
  }
}
