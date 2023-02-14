// let letterInput= document.getElementById("#potion").value();

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
        <div id="${potion.id}" class="card box text-center" style="height: 20rem">
            <a href="/potions/${potion.id}"><img class="card-img-top char-img img-fluid" src="${potion.image}"></a>
            <div class="card-body">
            <p class="card-text-center" style="font-size: .8rem">${potion.name}</p>
            </div>
        </div>
    </div>
`);
}

// const $potionLikeBtn = $("#potion-like");
// $potionLikeBtn.on("click", addLike);

// async function addLike(evt) {
//   const potionId = $("#potion-id");
//   const potionName = $("h2");
//   const potionImage = $("img");

//   potion = { potionName, potionImage };
//   resp = await axios.post(`/potions/${potionId}/like`, potion);

//   handleResponse(resp.data);
// }

// function handleResponse(data) {}

// Spells
