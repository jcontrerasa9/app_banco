<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http; // Esta clase nos permite realizar peticiones HTTP a otros servicios

class AccountController extends Controller
{

    private $variable = "Mensaje redireccionado desde el Gateway";

    public function example(){
        $response = Http::post("http://localhost:5000/example", [
            'dato'=> $this->variable
        ]);

        return response()->json($response->json(), $response->status());
    }
}
