ymaps.ready(init);
function init(){
    let myMap = new ymaps.Map("map", {
                center: [59.94, 30.39],
                zoom: 10
            }, {
            searchControlProvider: 'yandex#search'
            });

    BX24.callMethod('crm.company.list',{select:['TITLE','ID','ADDRESS_CITY','ADDRESS']}, function (comp) {
        let Companies = comp.answer.result
        Companies.forEach((company) => {
            let object = ymaps.geocode(`${company['ADDRESS_CITY']}, ${company['ADDRESS']}`)
            object.then(
            function (res) {
                let coor = res.geoObjects.properties._data.metaDataProperty.GeocoderResponseMetaData.Point.coordinates
                myMap.geoObjects.add(new ymaps.Placemark([coor[1], coor[0]], {balloonContent: `<strong>${company['TITLE']}</strong>` + '\n' + `${company['ADDRESS_CITY']}, ${company['ADDRESS']}`}, ));
            })
        })
        if (comp.more())
            comp.next()

    })
}