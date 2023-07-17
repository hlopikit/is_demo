ymaps.ready(init);
function init(){
    let myMap = new ymaps.Map("map", {
                center: [59.94, 30.39],
                zoom: 10
            }, {
            searchControlProvider: 'yandex#search'
            });

    BX24.callMethod('crm.company.list',{select:['TITLE','ID']}, function (comp) {
        let Companies = comp.answer.result
        BX24.callMethod('crm.address.list', {select: ['CITY', 'ADDRESS_1', 'ANCHOR_ID']}, function (result) {
                let Addresses = result.answer.result
                console.log(Addresses)
                console.log(Companies)
                Companies.forEach((company) => {
                    Addresses.forEach((address) => {
                        if (company['ID'] === address['ANCHOR_ID']) {
                            let object = ymaps.geocode(`${address['CITY']}, ${address['ADDRESS_1']}`)
                            object.then(
                            function (res) {
                                let coor = res.geoObjects.properties._data.metaDataProperty.GeocoderResponseMetaData.Point.coordinates
                                myMap.geoObjects.add(new ymaps.Placemark([coor[1], coor[0]], {balloonContent: `<strong>${company['TITLE']}</strong>` + '\n' + `${address['CITY']}, ${address['ADDRESS_1']}`}, ));
                            })
                        }
                    })
                })
            })
    })
}

