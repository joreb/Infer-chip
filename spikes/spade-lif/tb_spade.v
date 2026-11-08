module tb_spade;
  reg [7:0] v_i, acc_i, leak_i, threshold_i, rest_i;
  wire [8:0] out_o;
  spade_lif_wrapper dut (.v_i(v_i), .acc_i(acc_i), .leak_i(leak_i),
                           .threshold_i(threshold_i), .rest_i(rest_i), .out_o(out_o));

  integer i;
  reg [31:0] seed;
  initial begin
    seed = 32'hC0FFEE;
    $display("V A L T R O");
    for (i = 0; i < 20000; i = i + 1) begin
      v_i = $random(seed);
      acc_i = $random(seed);
      leak_i = $random(seed);
      threshold_i = $random(seed);
      rest_i = $random(seed);
      #1;
      $display("%0d %0d %0d %0d %0d %0d", v_i, acc_i, leak_i, threshold_i, rest_i, out_o);
    end
    $finish;
  end
endmodule
