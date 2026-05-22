package com.project.controller;

import jakarta.validation.Valid;

import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.project.exception.HttpException;
import com.project.model.Projekt;
import com.project.model.Student;
import com.project.model.Zadanie;
import com.project.service.ProjektService;
import com.project.service.StudentService;
import com.project.service.ZadanieService;

@Controller
public class ZadanieController {

    private ZadanieService zadanieService;
    private ProjektService projektService;
    private StudentService studentService;

    public ZadanieController(ZadanieService zadanieService, ProjektService projektService,
                             StudentService studentService) {
        this.zadanieService = zadanieService;
        this.projektService = projektService;
        this.studentService = studentService;
    }

    @GetMapping("/zadanieList")
    public String zadanieList(Model model, Pageable pageable,
                              @RequestParam(name = "projektId", required = false) Integer projektId) {
        if (projektId != null) {
            model.addAttribute("zadania", zadanieService.getZadaniaProjektu(projektId, pageable).getContent());
        } else {
            model.addAttribute("zadania", zadanieService.getZadania(pageable).getContent());
        }
        return "zadanieList";
    }

    @GetMapping("/zadanieEdit")
    public String zadanieEdit(@RequestParam(name = "zadanieId", required = false) Integer zadanieId, Model model) {
        if (zadanieId != null) {
            model.addAttribute("zadanie", zadanieService.getZadanie(zadanieId).get());
        } else {
            Zadanie zadanie = new Zadanie();
            model.addAttribute("zadanie", zadanie);
        }
        model.addAttribute("projekty", projektService.getProjekty(Pageable.unpaged()).getContent());
        return "zadanieEdit";
    }

    @PostMapping(path = "/zadanieEdit")
    public String zadanieEditSave(@ModelAttribute @Valid Zadanie zadanie, BindingResult bindingResult, Model model) {
        if (bindingResult.hasErrors()) {
            model.addAttribute("projekty", projektService.getProjekty(Pageable.unpaged()).getContent());
            return "zadanieEdit";
        }
        try {
            zadanie = zadanieService.setZadanie(zadanie);
        } catch (HttpException e) {
            bindingResult.rejectValue("nazwa", String.valueOf(e.getMessage()), e.getMessage());
            model.addAttribute("projekty", projektService.getProjekty(Pageable.unpaged()).getContent());
            return "zadanieEdit";
        }
        return "redirect:/zadanieList";
    }

    @PostMapping(params = "cancel", path = "/zadanieEdit")
    public String zadanieEditCancel() {
        return "redirect:/zadanieList";
    }

    @PostMapping(params = "delete", path = "/zadanieEdit")
    public String zadanieEditDelete(@ModelAttribute Zadanie zadanie) {
        zadanieService.deleteZadanie(zadanie.getZadanieId());
        return "redirect:/zadanieList";
    }
}
