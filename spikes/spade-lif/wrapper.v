module spade_lif_wrapper (
    input  wire [7:0] v_i,
    input  wire [7:0] acc_i,
    input  wire [7:0] leak_i,
    input  wire [7:0] threshold_i,
    input  wire [7:0] rest_i,
    output wire [8:0] out_o
);
    \spade_lif_spike::main u (
        .v_i(v_i),
        .acc_i(acc_i),
        .leak_i(leak_i),
        .threshold_i(threshold_i),
        .rest_i(rest_i),
        .output__(out_o)
    );
endmodule
