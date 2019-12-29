$path_runFile = ".\SemantickiAnalizator.py"


#pgombar test files

echo "test files"
$path_testDirectories = "C:\Users\Ayakuro\Documents\Work\ppj_test\PPJ\labos3\primjeri\"
$testDir = @("01_idn", "02_broj", "03_niz_znakova", "04_pogresan_main", "05_impl_int2char", "06_nedekl_fun", "07_nedef_fun", "08_ne_arg", "09_fun_povtip", "10_fun_params", "11_niz", "12_fun_niz", "13_lval1", "14_lval2", "15_cast1", "16_cast2", "17_log", "18_if", "19_cont_brk", "20_ret_void", "21_ret_nonvoid", "22_fun_multidef", "23_rek", "24_param_dekl", "25_fun_dekl_def", "26_multi_dekl", "27_dekl_odmah_aktivna", "28_niz_init", "29_for", "30_const_init")

foreach ($dir in $testDir) {
    
    $test_result = & Get-Content ($path_testDirectories + $dir + "\test.in") | python $path_runFile
    $test_result = $test_result.Trim()

    $correct_result = Get-Content ($path_testDirectories + $dir + "\test.out")
    $correct_result = $correct_result.Trim()

    if ($test_result -eq $correct_result) {
        "ok"
    }
    else {
        "error"
    }
}

$test_result = & Get-Content ($path_testDirectories + "integration" + "\main.in") | python $path_runFile
$test_result = $test_result.Trim()

$correct_result = Get-Content ($path_testDirectories + "integration" + "\main.out")
$correct_result = $correct_result.Trim()

if ($test_result -eq $correct_result) {
    "ok"
}
else {
    "error"
}

$test_result = & Get-Content ($path_testDirectories + "integration" + "\array.in") | python $path_runFile
$test_result = $test_result.Trim()

$correct_result = Get-Content ($path_testDirectories + "integration" + "\array.out")
$correct_result = $correct_result.Trim()

if ($test_result -eq $correct_result) {
    "ok"
}
else {
    "error"
}