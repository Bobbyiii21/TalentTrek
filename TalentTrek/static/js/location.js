async function initAutocomplete() {
const { PlaceAutocompleteElement } =
    await google.maps.importLibrary("places");

const autocomplete = new PlaceAutocompleteElement();

autocomplete.id = "autocomplete";
autocomplete.placeholder = "Start typing an address...";

document.getElementById("autocomplete-container").appendChild(autocomplete);

autocomplete.addEventListener("gmp-select", async ({ placePrediction }) => {
    const place = placePrediction.toPlace();

    await place.fetchFields({
    fields: [
        "displayName",
        "formattedAddress",
        "addressComponents",
        "location",
    ],
    });

    const components = place.addressComponents;

    function get(type) {
    const comp = components.find((c) => c.types.includes(type));
    return comp ? comp.longText : "";
    }

    document.getElementById("street").value =
    get("street_number") + " " + get("route");

    document.getElementById("city").value = get("locality");
    document.getElementById("state").value = get(
    "administrative_area_level_1",
    );

    document.getElementById("postal_code").value = get("postal_code");

    document.getElementById("country").value = get("country");

    document.getElementById("latitude").value = place.location.lat();

    document.getElementById("longitude").value = place.location.lng();
});
}

window.initAutocomplete = initAutocomplete;