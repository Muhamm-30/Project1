
`default_nettype none

module matrix_core (
    input wire clk,
    input wire rst_n,
    input wire clear,
    input wire enable,

    // One column of A per cycle
    input wire signed [3:0] a0,
    input wire signed [3:0] a1,

    // One row of B per cycle
    input wire signed [3:0] b0,
    input wire signed [3:0] b1,

    // Four matrix results
    output wire signed [11:0] c00,
    output wire signed [11:0] c01,
    output wire signed [11:0] c10,
    output wire signed [11:0] c11
);

    mac_unit mac00 (
        .clk(clk),
        .rst_n(rst_n),
        .clear(clear),
        .enable(enable),
        .a(a0),
        .b(b0),
        .acc(c00)
    );

    mac_unit mac01 (
        .clk(clk),
        .rst_n(rst_n),
        .clear(clear),
        .enable(enable),
        .a(a0),
        .b(b1),
        .acc(c01)
    );

    mac_unit mac10 (
        .clk(clk),
        .rst_n(rst_n),
        .clear(clear),
        .enable(enable),
        .a(a1),
        .b(b0),
        .acc(c10)
    );

    mac_unit mac11 (
        .clk(clk),
        .rst_n(rst_n),
        .clear(clear),
        .enable(enable),
        .a(a1),
        .b(b1),
        .acc(c11)
    );

endmodule

`default_nettype wire
