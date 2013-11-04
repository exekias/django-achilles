
module("blocks");
test("get", function() {
    achilles = achilles('/endpoint/');

    equal(achilles.blocks('test').length, 1, "got one block");

    deepEqual(achilles.blocks('test')[0], $('[data-ablock=test]')[0],
              "got correct block");
});


module("actions");
test("TODO", function() {
    ok( "TODO" == "TODO");
});
