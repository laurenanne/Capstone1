// Potions
const $search = $("#search-addon");
$search.on("click", getPotions);

async function getPotions(evt) {
  const input = $("#potion-input")[0].value;
  resp = await axios.get(`/potions/search/${input}`);
  response = resp.data;
  putPotionsOnPage(response);
}

function putPotionsOnPage(resp) {
  const $potionContainer = $("#potion-results");
  $potionContainer.empty();
  for (let i = 0; i < resp.length; i++) {
    let $potion = generatePotionMarkup(resp[i]);
    $potionContainer.append($potion);
  }
  $potionContainer.show();
}

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

// Spells
const $searchSpells = $("#search-spells");
$searchSpells.on("click", getSpells);

async function getSpells(evt) {
  const input = $("#spell-input")[0].value;
  resp = await axios.get(`/spells/search/${input}`);
  response = resp.data;
  putSpellsOnPage(response);
}

function putSpellsOnPage(resp) {
  const $spellContainer = $("#spell-results");
  $spellContainer.empty();
  for (let i = 0; i < resp.length; i++) {
    let $spell = generateSpellMarkup(resp[i]);
    $spellContainer.append($spell);
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
