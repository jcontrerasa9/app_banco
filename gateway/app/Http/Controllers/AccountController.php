<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Client\ConnectionException; // Clase para el manejo de errores por conexion al microservicio
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

    private const ACCOUNTS_URL = 'http://localhost:5000/api/accounts';

    public function index()
    {
        return $this->forward(fn () => Http::timeout(5)->get(self::ACCOUNTS_URL));
    }

    public function show(int $account)
    {
        return $this->forward(fn () => Http::timeout(5)->get(self::ACCOUNTS_URL . '/' . $account));
    }

    public function store(Request $request)
    {
        return $this->forward(fn () => Http::timeout(5)->post(self::ACCOUNTS_URL, $request->all()));
    }

    public function update(Request $request, int $account)
    {
        return $this->forward(fn () => Http::timeout(5)->put(
            self::ACCOUNTS_URL . '/' . $account,
            $request->all()
        ));
    }

    public function destroy(int $account)
    {
        return $this->forward(fn () => Http::timeout(5)->delete(self::ACCOUNTS_URL . '/' . $account));
    }

    // forward ejecuta la peticion que con callable cada metodo le pasa.
    // Ya que todos despues de la peticion, tienen que repetir el manejo de errores, status, etc.
    private function forward(callable $request)
    {
        try {
            $response = $request();

            if ($response->status() === 204) {
                return response()->noContent();
            }

            return response()->json($response->json(), $response->status());
        } catch (ConnectionException $exception) {
            return response()->json([
                'error' => 'No se pudo conectar con el microservicio de cuentas',
            ], 503);
        }
    }
}
