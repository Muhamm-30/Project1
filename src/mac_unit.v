
`default_nettype none

module mac_unit (
    input  wire clk,
    input  wire rst_n,
    input  wire clear,
    input  wire enable,

    input  wire signed [3:0] a,
    input  wire signed [3:0] b,

    output reg signed [11:0] acc
);

    wire signed [7:0] product;
    wire signed [11:0] extended_product;

    // Signed 4-bit x 4-bit multiplication
    assign product = a * b;

    // Sign extend the product to 12 bits
    assign extended_product = {{4{product[7]}}, product};

    // Accumulate once per enabled clock cycle
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            acc <= 12'sd0;
        else if (clear)
            acc <= 12'sd0;
        else if (enable)
            acc <= acc + extended_product;
    end

endmodule

`default_nettype wire
