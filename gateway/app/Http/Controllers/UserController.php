<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class UserController extends Controller
{
    public function register(Request $request){
        // Lógica para registrar un nuevo usuario
        $user = User::create($request->all());

        return response()->json($user, 201);
    }   
}
