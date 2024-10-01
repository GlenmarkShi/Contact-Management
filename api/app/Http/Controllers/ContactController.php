<?php

namespace App\Http\Controllers;

use App\Models\Contact;
use Illuminate\Http\Request;

class ContactController extends Controller
{
    public function upload(Request $request)
    {
        $request->validate([
            'file' => 'required|mimes:json'
        ]);

        // Store the file in the storage/app/contacts folder
        $path = $request->file('file')->store('contacts');
        return response()->json(['path' => $path], 200);
        //return response()->json(null, 204);
    }

    public function index(Request $request)
    {
        $query = Contact::query();

        if ($request->has('search')) {
            $query->where(function ($q) use ($request) {
                $q->where('name', 'like', '%' . $request->search . '%')
                  ->orWhere('email', 'like', '%' . $request->search . '%');
            });
        }

        $contacts = $query->paginate(10);
        return response()->json($contacts);
    }

    public function show($id)
    {
        $contact = Contact::find($id);
        return response()->json($contact);
    }

    public function update(Request $request, $id)
    {
        $contact = Contact::find($id);
        $contact->update($request->all());
        return response()->json($contact);
    }

    public function delete($id)
    {
        Contact::destroy($id);
        return response()->json(['message' => 'Contact deleted']);
    }
}
