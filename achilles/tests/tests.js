
module("blocks");
test("get", function() {
    achilles = achilles('/endpoint/');

    equal(achilles.blocks.get('test').length, 1, "got one block");

    deepEqual(achilles.blocks.get('test')[0], $('[data-ablock=test]')[0],
              "got correct block");
});


module("actions");
test("get", function() {
    ok( "TODO" == "TODO");
});
